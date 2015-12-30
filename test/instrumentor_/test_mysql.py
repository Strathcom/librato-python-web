# Copyright (c) 2015. Librato, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Librato, Inc. nor the names of project contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL LIBRATO, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import unittest

import MySQLdb

from librato_python_web.instrumentor import telemetry
from librato_python_web.instrumentor.context import add_tag, push_state, pop_state

from test_reporter import TestTelemetryReporter


class MysqlTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def run_queries(self):
        # connect (params impl dependent) dsn data source name, host hostname, database db name
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="root", db="test")

        # Exception logging (see types: https://www.python.org/dev/peps/pep-0249/#exceptions)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.execute("SELECT 1 FROM DUAL")
        cur.executemany("SELECT 1 FROM DUAL", [None, None, None, None, None])

        # callproc

        try:
            cur.execute("drop procedure usercount")
        except:
            pass   # proc might not exist

        cur.execute("create procedure usercount() begin select count(*) from mysql.user; end")
        cur.callproc("usercount", ())

        cur.close()		# To avert an out of sync error
        cur = conn.cursor()

        cur.callproc("usercount", ())

        # fetchmany
        # nextset???

        # tpc extensions???

        cur.close()

    def test_mysql(self):
        reporter = TestTelemetryReporter()
        telemetry.set_reporter(reporter)

        with add_tag('test-context', 'mysql_test'):
            try:
                push_state('web')
                self.run_queries()
            finally:
                pop_state('web')

        self.assertTrue(reporter.counts)
        self.assertTrue(reporter.records)

        print reporter.counts
        print reporter.records

    def test_mysql_nostate(self):
        reporter = TestTelemetryReporter()
        telemetry.set_reporter(reporter)

        with add_tag('test-context', 'mysql_test'):
            self.run_queries()

        self.assertFalse(reporter.counts)
        self.assertFalse(reporter.records)
        print reporter.counts
        print reporter.records

if __name__ == '__main__':
    unittest.main()