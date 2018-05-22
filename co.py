"""
Usage:
    exe <command>
"""

from docopt import docopt
args = docopt(__doc__)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ls.settings")
import django
django.setup()

from django.db.utils import DatabaseError

from django.db.models.sql.compiler import SQLCompiler

class LsCompiler(SQLCompiler):

    def as_sql(self, with_limits=True, with_col_aliases=False):
        extra_select, order_by, group_by = self.pre_sql_setup()
        for_update_part = None
        combinator = self.query.combinator
        features = self.connection.features
        if combinator:
            if not getattr(features, 'supports_select_{}'.format(combinator)):
                raise DatabaseError('{} not supported on this database backend.'.format(combinator))
            result, params = self.get_combinator_sql(combinator, self.query.combinator_all)
        else:
            distinct_fields = self.get_distinct()

        result = ['SELECT']
        params = []

        if self.query.distinct:
            result.append(self.connection.ops.distinct_sql(distinct_fields))

        out_cols = []
        col_idx = 1
        for _, (s_sql, s_params), alias in self.select + extra_select:
            if alias:
                s_sql = '%s AS %s' % (s_sql, self.connection.ops.quote_name(alias))
            elif with_col_aliases:
                s_sql = '%s AS %s' % (s_sql, 'Col%d' % col_idx)
                col_idx += 1
            params.extend(s_params)
            out_cols.append(s_sql)

        result.append(', '.join(out_cols))
        import ipdb; ipdb.set_trace()
        return result


def a():
    from django.db import DEFAULT_DB_ALIAS
    from ap.models import P
    qs = P.objects.filter(name='s')
    co = qs.query.get_compiler(using=DEFAULT_DB_ALIAS)
    co.__class__ = LsCompiler
    print(co.as_sql())

import co

if __name__ == '__main__':
    method = args['<command>']
    getattr(co, method)()