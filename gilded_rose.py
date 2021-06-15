# -*- coding: utf-8 -*-

def _mod_quality(item, inc=1):
    q = item.quality + inc
    if q > 50: q = 50
    if q <0: q = 0
    return q

def _aged_normal(item):
    return Item(item.name, item.sell_in - 1, _mod_quality(item, -1))

def _aged_conjured(item):
    return Item(item.name, item.sell_in - 1, _mod_quality(item, -2))

def _aged_brie(item):
    return Item(item.name, item.sell_in - 1, _mod_quality(item, 1))

def _aged_backstage(item):
    def aged_quality_backstage(item):
        if item.sell_in > 10:
            return _mod_quality(item, 1)
        elif item.sell_in > 5:
            return _mod_quality(item, 2)
        elif item.sell_in > 0:
            return _mod_quality(item, 3)
        else:
            return _mod_quality(item, -item.quality)
    return Item(item.name, item.sell_in - 1, aged_quality_backstage(item))

def _aged_sulfuras(item):
    return Item(item.name, item.sell_in, item.quality)

def _aged(item):
        item_ager = {
            Item.NAMES.AGED_BRIE:        _aged_brie,
            Item.NAMES.CONJURED:         _aged_conjured,
            Item.NAMES.BACKSTAGE_PASSES: _aged_backstage,
            Item.NAMES.SULFURAS:         _aged_sulfuras,
        }.get(item.name, _aged_normal)
        return item_ager(item)

def update_quality(items):
    return [_aged(item) for item in items]


class Item:
    class NAMES:
        AGED_BRIE = "Aged Brie"
        CONJURED = "Conjured Mana Cake"
        BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
        SULFURAS = "Sulfuras, Hand of Ragnaros"

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    def __eq__(self, other):
        return repr(self) == repr(other)

