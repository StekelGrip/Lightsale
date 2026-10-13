# Disable legacy module UI and scheduled jobs before the dummy update.
# Only records identified by this module's external IDs are touched.
def migrate(cr, version):
    module = 'stock_move_location'
    for table, model in (("ir_ui_view", "ir.ui.view"),
                         ("ir_ui_menu", "ir.ui.menu"),
                         ("ir_cron", "ir.cron")):
        cr.execute("SELECT to_regclass(%s)", (table,))
        if not cr.fetchone()[0]:
            continue
        cr.execute("""SELECT 1 FROM information_schema.columns
                      WHERE table_schema = current_schema()
                      AND table_name = %s AND column_name = 'active'""", (table,))
        if not cr.fetchone():
            continue
        cr.execute(
            "UPDATE " + table + " SET active = FALSE WHERE id IN "
            "(SELECT res_id FROM ir_model_data WHERE module = %s AND model = %s)",
            (module, model),
        )
