resources = set(['wood', 'stone', 'ore', 'brick', 'glass', 'papyrus', 'cloth', 'gold'])
science = set(['gear', 'compass', 'tablet'])
colors = set(['blue', 'red', 'yellow', 'gray', 'green', 'purple'])


class Card(object):
    def __init__(self, name, cost, color, effect=None, resources=None,
                 exotic=None, science=None, military=None, coupons=None):
        '''

        :param name: name of card (str)
        :param cost: cost dict
        :param color: card color (str)
        :param effect: unique effect (function)
        :param resources: resources given (dict)
        :param exotic: exotic resource given (Exotic)
        :param science: science symbols given (dict)
        :param military: military given (int)
        :param coupons: coupons given (list of str)
        '''
        self.cost = cost
        if effect is not None:
            self.effect = effect
        else:
            self.effect = lambda x: None
        self.color = color
        self.name = name
        self.resources = resources
        self.exotic = exotic
        self.science = science
        self.military = military
        self.coupons = coupons


class Player(object):
    def __init__(self, name, wonder, game, ai):
        self.name = name
        self.wonder = wonder
        self.wonder.init(self, game)
        self.game = game
        self.ai = ai

        self.military = 0
        self.resources = dict((k, 0) for k in resources)
        self.science = dict((k, 0) for k in science)
        self.colors = dict((k, 0) for k in colors)
        self.exotic_resources = []
        self.temporary_resources = dict((k, 0) for k in resources)
        self.coupons = []
        self.buy_costs = {'brown': {'left': 2, 'right': 2},
                          'gray': {'left': 2, 'right': 2}}
        self.vp = 0
        self.defeats = 0
        self.tableau = []

    def play(self, card):
        assert self.can_build(card)
        self.colors[card.color] += 1
        self.resources['gold'] -= card.cost.get('gold', 0)
        card.effect(self)
        if card.resources:
            for r, n in card.resources.iteritems():
                self.resources[r] += n
        if card.exotic:
            self.exotic_resources.append(card.exotic)
        if card.science:
            for s, n in card.science.iteritems():
                self.science[s] += n
        if card.military:
            self.military += card.military
        if card.coupons:
            self.coupons += card.coupons
        self.tableau.append(card)

    def discard(self, card):
        self.resources['gold'] += 3

    def wonder(self, card):
        self.wonder.build(self)

    def can_build(self, card):
        if card.name in self.coupons:
            return True
        else:
            return self.has_resources(card.cost)

    def has_resources(self, resources):
        '''
        Checks if a player has the resources indicated in the resources param
        :param resources: dict of {resource: int} indicating resources requested
        :return: bool
        '''
        def all_satisfied(needed):
            '''
            helper to check that all resource needs have been satisfied
            :param needed: updated needed resources dict
            :return: bool
            '''
            return all([v <= 0 for v in needed.values()])

        def exotic_check(needed, resources):
            '''
            helper to recursively search exotic resources
            :param needed: resources still needed (dict)
            :param resources: list of exotic resources available
            :return: bool
            '''
            # Base case
            if all_satisfied(needed):
                return True

            # Inductive case
            # iterate through resources
            for idx, e in enumerate(resources):
                # remove currently examined resource
                resource_copy = resources[:]
                resource_copy.pop(idx)
                # try providing a resource of each type it gives
                for r in e.can_provide:
                    new_needed = needed.copy()
                    if r in new_needed:
                        new_needed[r] -= 1
                    if exotic_check(new_needed, resource_copy):
                        return True
            return False

        needed = resources.copy()
        for k, v in self.resources.iteritems():
            if k in needed:
                needed[k] -= v
        if all_satisfied(needed):
            return True
        return exotic_check(needed, self.exotic_resources)


class Exotic(object):
    def __init__(self, can_provide):
        self.can_provide = set(can_provide)


class Wonder(object):
    def __init__(self, resource):
        self.resource = resource
        self.stage = 0

    def init(self, player, game):
        player.resources[self.resource] += 1
        self.game = game

class Game(object):
    def __init__(self):
        pass



p = Player('me')
p.exotic_resources += [Exotic(['wood', 'brick']), Exotic(['wood', 'stone', 'ore', 'brick']), Exotic(['wood', 'ore'])]
print p.has_resources({'brick': 2, 'ore': 1})
print p.has_resources({'ore': 2, 'stone': 1})
