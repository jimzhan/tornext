#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import UIModule


class Login(UIModule):

    def render(self):
        return self.render_string('modules/login.html')
