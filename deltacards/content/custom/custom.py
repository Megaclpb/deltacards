from deltacards.dsl.api import *

BASE_ID = 10000

@card(
    BASE_ID,
    name="Ferroll",
    description="{{KW:MAGIC}}: {{KW:ERASE}} a card with a base {{COST}} of 2+ {{GOLD}} in your hand to deal 2 {{DMG}} to all enemies.",
    cost=7,
    attack=7,
    hp=6,
    rarity=EPIC,
    image=CustomImage("images/Ferroll.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Ferroll{{PLURAL:$1||s}}",
            description="{{KW:MAGIC}}: {{KW:ERASE}} a card with a base {{COST}} of 2+ {{GOLD}} in your hand to deal 2 {{DMG}} to all enemies.",
        ),
    },
)
class Ferroll(Monster):
    targets = HAND

    magic = TARGET.erase().to(
        ENEMIES.hit(2)
    )

@card(
    BASE_ID+1,
    name="Diamond King",
    description="{{KW:MAGIC}}: Draw a card for each other ally monster. Give them -1 {{COST}} for each spell you spent {{GOLD}} on this turn.",
    cost=5,
    attack=4,
    hp=6,
    rarity=EPIC,
    image=CustomImage("images/Diamond_King.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Diamond King{{PLURAL:$1||s}}",
            description="{{KW:MAGIC}}: Draw a card for each other ally monster. Give them -1 {{COST}} for each spell you spent {{GOLD}} on this turn.",
        ),
    },
)
class DiamondKing(Monster):
    draw_result: Var[StepResult] = Var(StepResult)

    magic = (
        For(
            COUNT(ALLY_MONSTERS & ~SELF),
            YOU.draw_next().store_result(draw_result).to(
                Buff(target=draw_result.card_id, cost=-COUNT(GOLD_SPENT(player=YOU, scope=THIS_TURN, reason='play_spell')))
            )
        )
    )


@card(
    BASE_ID+2,
    name="Vampire Alvin",
    description="{{KW:MAGIC}} and {{KW:SHOCK}}: Give all enemy monsters -1 {{HP}}. Give yourself the {{HP}} reduced.",
    cost=7,
    attack=7,
    hp=7,
    rarity=EPIC,
    image=CustomImage("images/Vampire_Alvin.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Vampire Alvin{{PLURAL:$1||s}}",
            description="{{KW:MAGIC}} and {{KW:SHOCK}}: Give all enemy monsters -1 {{HP}}. Give yourself the {{HP}} reduced.",
        ),
    },
)
class VampireAlvin(Monster):
    monster: Var[StepResult] = Var(StepResult)

    _effect = ForEach(
        ENEMY_MONSTERS,
        var=monster,
        effect=monster.buff(hp=-1).to(
            YOU.buff(hp=+1)
        )
    )

    magic = _effect
    shock = _effect


@card(
    BASE_ID+3,
    name="Dunked Mascot",
    description="{{KW:HASTE}}. After this takes {{DMG}}, this {{CARD:72|override=Melts}}.",
    cost=6,
    attack=3,
    hp=6,
    keywords=HASTE,
    rarity=COMMON,
    image=CustomImage("images/Dunked_Mascot.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Dunked Mascot{{PLURAL:$1||s}}",
            description="{{KW:HASTE}}. After this takes {{DMG}}, this {{CARD:72|override=Melts}}.",
        ),
    },
)
class DunkedMascot(Monster):
    @on_event(EntityDamagedResult)
    def on_entity_damaged(self, res: EntityDamagedResult, game, **kwargs):
        if res.target_id != self.id:
            return None

        return Cast(
                card=GENERATE_CARD("Melt"),
                controller=YOU,
                effect_target=SELF
            )


@card(
    BASE_ID+4,
    name="Balthizard",
    description="{{KW:ARMOR}}. {{KW:MAGIC}}: Summon 3 {{CARD:615|3}}. {{KW:DELAY}}: {{KW:ERASE}} all ally {{CARD:615|2}} to gain {{STATS:+1|+2}} for each.",
    cost=9,
    attack=4,
    hp=4,
    rarity=EPIC,
    image=CustomImage("images/Balthizard.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Balthizard{{PLURAL:$1||s}}",
            description="{{KW:ARMOR}}. {{KW:MAGIC}}: Summon 3 {{CARD:615|3}}. {{KW:DELAY}}: {{KW:ERASE}} all ally {{CARD:615|2}} to gain {{STATS:+1|+2}} for each.",
        ),
    },
)
class Balthizard(Monster):
    X: Var[Card] = Var(Card)

    magic = (
        GENERATE_CARD("Toxic Cloud").summon() * 3
        >> SELF.schedule_delay_effect()
    )

    delay = ForEach(
        ALLY_MONSTERS & (TEMPLATE_NAME == "Toxic Cloud"),
        var=X,
        effect=X.erase().to(SELF.buff(attack=+1, hp=+2))
    )


@card(
    BASE_ID+5,
    name="Royal Water Bottle",
    description="{{KW:MAGIC}}: Summon a {{CARD:237}} with {{KW:HASTE}}. {{KW:DELAY}}: If its dead, summon one with {{KW:TAUNT}}",
    cost=8,
    attack=3,
    hp=3,
    rarity=RARE,
    image=CustomImage("images/Royal_Water_Bottle.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Royal Water Bottle{{PLURAL:$1||s}}",
            description="{{KW:MAGIC}}: Summon a {{CARD:237}} with {{KW:HASTE}}. {{KW:DELAY}}: If its dead, summon one with {{KW:TAUNT}}",
        ),
    },
)
class RoyalWaterBottle(Monster):
    summon_result: Var[StepResult] = Var(StepResult)
    generated_card: Var[TargetSelector] = Var(TargetSelector)

    magic = (
        SetVar(var=generated_card, value=GENERATE_CARD("Punk Hamster"))
        >> generated_card.add_keyword(HASTE)
        >> generated_card.summon().store_result(summon_result)
        >> SELF.schedule_delay_effect()
    )

    delay = Check(RESOLVE_ENTITY(summon_result.monster_id).dead).to(
        SetVar(var=generated_card, value=GENERATE_CARD("Punk Hamster"))
        >> generated_card.add_keyword(TAUNT)
        >> generated_card.summon()
    )


@card(
    BASE_ID+6,
    name="Terakota2",
    description="{{KW:HASTE}}. {{KW:ARMOR}}. After this takes {{DMG}} and {{KW:DUST}}: Summon a {{CARD:375|1}} with {{KW:HASTE}}",
    cost=9,
    attack=6,
    hp=8,
    keywords=ARMOR | HASTE,
    tribes=[Tribe.PLANT],
    rarity=RARE,
    image=ExistingImage("Terakota"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Terakota{{PLURAL:$1||s}}",
            description="{{KW:HASTE}}. {{KW:ARMOR}}. After this takes {{DMG}} and {{KW:DUST}}: Summon a {{CARD:375|1}} with {{KW:HASTE}}",
        ),
    },
)
class Terakota2(Monster):
    generated_card: Var[TargetSelector] = Var(TargetSelector)
    _effect = (
        SetVar(var=generated_card, value=GENERATE_CARD("Green Clover"))
        >> generated_card.add_keyword(HASTE)
        >> generated_card.summon()
    )

    dust = _effect
    @on_event(EntityDamagedResult)
    def on_entity_damaged(self, res: EntityDamagedResult, game, **kwargs):
        if res.target_id != self.id:
            return None

        return self._effect

@card(
    BASE_ID+7,
    name="Samurai Guard",
    description="{{KW:ARMOR}}. {{KW:DELAY}}: Halve the stats of all monsters with a base {{cost}} of 9 or less {{GOLD}} in your hand.",
    cost=9,
    attack=7,
    hp=7,
    keywords=ARMOR,
    tribes=[Tribe.ROYAL_GUARD],
    rarity=EPIC,
    image=CustomImage("images/Samurai_Guard.png"),
    expansion=Expansion.BASE,
    localizations={
        'en': LocalizedText(
            name="Samurai Guard{{PLURAL:$1||s}}",
            description="{{KW:ARMOR}}. {{KW:DELAY}}: Halve the stats of all monsters with a base {{cost}} of 9 or less {{GOLD}} in your hand.",
        ),
    },
)
class SamuraiGuard(Monster):
    X: Var[Card] = Var(Card)

    magic = SELF.schedule_delay_effect()

    delay = ForEach(
        HAND & IS_MONSTER,
        var=X,
        effect=(
            X.halve_stats(round_up=True, halve_cost=True)
        )
    )

@card(
    BASE_ID+8,
    name="Cowgirl Susie",
    description="{{KW:HASTE}}. Before this attacks a monster, make it {{KW:WANTED}}. {{KW:MAGIC}}: Summon an enemy {{CARD:136|1}}.",
    cost=6,
    attack=6,
    hp=8,
    keywords=HASTE,
    rarity=EPIC,
    image=CustomImage("images/Cowgirl_Susie.png"),
    expansion=Expansion.DELTARUNE,
    localizations={
        'en': LocalizedText(
            name="Cowgirl Susie{{PLURAL:$1||s}}",
            description="{{KW:HASTE}}. Before this attacks a monster, make it {{KW:WANTED}}. {{KW:MAGIC}}: Summon an enemy {{CARD:136|1}}.",
        ),
    },
)
class CowgirlSusie(Monster):
    magic = GENERATE_CARD("Cactus", controller=OPPONENT).summon(controller=OPPONENT)

    @on_event(AttackDeclaredResult)
    def on_attack_declared(self, res: AttackDeclaredResult, game, **kwargs):
        if res.attacker_id != self.id:
            return None

        return AddKeyword(target=res.defender_id, keyword=WANTED)