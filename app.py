#!/usr/bin/env python3

from aws_cdk import core

from valhalla_bot.valhalla_bot_stack import ValhallaBotStack


app = core.App()
ValhallaBotStack(app, "valhalla-bot")

app.synth()
