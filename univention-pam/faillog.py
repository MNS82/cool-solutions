#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Univention PAM
#  Listener module for faillog
#
# Copyright 2001-2015 Univention GmbH
#
# http://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

name='faillog'
description='The listener module resets the faillog count'
filter='objectClass=shadowAccount'
attributes=[]

__package__='' 	# workaround for PEP 366
import listener, os, sys, string
import univention.debug as ud

def __pwd_is_locked(password):
	if password.startswith('{crypt}!') or password.startswith('{LANMAN}!'):
		return True
	return False

def handler(dn, new, old):
	if new and old:
		new_password = new.get('userPassword', [None])[0]
		old_password = old.get('userPassword', [None])[0]
		if new_password and old_password:
			if __pwd_is_locked(old_password) and not __pwd_is_locked(new_password):
				#reset bad password cound
				listener.setuid(0)
				try:
					ud.debug(ud.LISTENER, ud.PROCESS, 'Reset faillog for user %s' % new['uid'][0])
					listener.run('/sbin/pam_tally', ['pam_tally', '--user', new['uid'][0], '--reset'])
				finally:
					listener.unsetuid()

def initialize():
	pass

