# Generated by Django 2.2.4 on 2020-02-03 14:02

from django.db import migrations, models, connections, DEFAULT_DB_ALIAS


class Migration(migrations.Migration):

    dependencies = [("input", "0044_squashed_60")]

    def recreateConstraintsCascade(apps, schela_editor):
        def getConstraint(cursor, tableName):
            cursor.execute(
                """
            select conname from pg_constraint
            inner join pg_class opplan on opplan.oid = pg_constraint.confrelid and opplan.relname = 'operationplan'
            inner join pg_class opm on opm.oid = pg_constraint.conrelid and opm.relname = %s
            inner join pg_attribute on attname = 'operationplan_id' and attrelid = opm.oid and pg_attribute.attnum = any(conkey)
            """,
                (tableName,),
            )
            return cursor.fetchone()[0]

        cursor = connections[DEFAULT_DB_ALIAS].cursor()
        cursor.execute(
            "alter table operationplanmaterial drop constraint %s"
            % (getConstraint(cursor, "operationplanmaterial"),)
        )
        cursor.execute(
            "alter table operationplanresource drop constraint %s"
            % (getConstraint(cursor, "operationplanresource"),)
        )
        cursor.execute(
            """
            alter table operationplanresource
            ADD FOREIGN KEY (operationplan_id)
            REFERENCES public.operationplan (reference) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
            DEFERRABLE INITIALLY DEFERRED
        """
        )
        cursor.execute(
            """
        alter table operationplanmaterial
            ADD FOREIGN KEY (operationplan_id)
            REFERENCES public.operationplan (reference) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE CASCADE
            DEFERRABLE INITIALLY DEFERRED
        """
        )

    operations = [migrations.RunPython(recreateConstraintsCascade)]
