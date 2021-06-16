# -*- coding: utf-8 -*-

from functools import partial

def _modify_quality(item, by=1):
    q = item.quality + by
    if q > 50: q = 50
    if q <0: q = 0
    return q

def _aged(item):
    if item.name == Item.NAMES.AGED_BRIE:
        return Item.create_brie(item.sell_in - 1, _modify_quality(item, by=1))

    if item.name == Item.NAMES.CONJURED:
        return Item.create_conjured(item.sell_in - 1, _modify_quality(item, by=-2))

    if item.name == Item.NAMES.BACKSTAGE_PASSES:
        def _aged_quality_backstage(item):
            if item.sell_in > 10:
                return _modify_quality(item, by=1)
            if item.sell_in > 5:
                return _modify_quality(item, by=2)
            if item.sell_in > 0:
                return _modify_quality(item, by=3)
            return _modify_quality(item, by=-item.quality)
        return Item.create_backstage(item.sell_in - 1, _aged_quality_backstage(item))

    if item.name == Item.NAMES.SULFURAS:
        return Item.create_sulfuras(item.sell_in, item.quality)

    return Item.create_normal(item.name, item.sell_in - 1, _modify_quality(item, by=-1))

def update_quality(items):
    return [_aged(item) for item in items]


class Item:
    class NAMES:
        AGED_BRIE = "Aged Brie"
        CONJURED = "Conjured Mana Cake"
        BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
        SULFURAS = "Sulfuras, Hand of Ragnaros"

    @classmethod
    def create_normal(cls, name, sell_in, quality):
        return cls(name, sell_in, quality)

    @classmethod
    def create_conjured(cls, sell_in, quality):
        return cls(cls.NAMES.CONJURED, sell_in, quality)

    @classmethod
    def create_brie(cls, sell_in, quality):
        return cls(cls.NAMES.AGED_BRIE, sell_in, quality)

    @classmethod
    def create_sulfuras(cls, sell_in, quality):
        return cls(cls.NAMES.SULFURAS, sell_in, quality)

    @classmethod
    def create_backstage(cls, sell_in, quality):
        return cls(cls.NAMES.BACKSTAGE_PASSES, sell_in, quality)

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    def __eq__(self, other):
        return repr(self) == repr(other)

