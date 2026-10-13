# Temporary dummy transition, authored by Grip ICT BV.
def migrate(cr, version):
    # Only disable records owned by this module. No business record SQL deletion.
    for table, model in (
        ("ir_ui_view", "ir.ui.view"),
        ("ir_ui_menu", "ir.ui.menu"),
        ("ir_cron", "ir.cron"),
    ):
        cr.execute(
            "UPDATE " + table + " SET active = FALSE WHERE id IN "
            "(SELECT res_id FROM ir_model_data WHERE module = %s AND model = %s)",
            ('sale_automatic_workflow', model),
        )
