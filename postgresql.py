# 2014, Shivani Gowrishankar <s.gowrishankar@ntoggle.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import psycopg2

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    """

    postgresql module used to query tables in postgresql database.

    Example: lookup('postgresql','database,username,password,SQL query')

    """
    def run(self, terms, variables, **kwargs):

        if not isinstance(terms, list):
            terms = [ terms ]

        ret = []
        for term in terms:
            (database,user,password,sql) = term.split(',')

        con = None
        con = psycopg2.connect(database=database, user=user, password=password)
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            row_string = str(row)
            ret.append(row_string)
        return ret