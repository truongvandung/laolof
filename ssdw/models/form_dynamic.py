from openerp import fields, models, api
from lxml import etree


class SUFormDynamic(models.Model):
    _name = "form.dynamic"

    fields_show = fields.Char(string="Fields Show", default="[]")
    model = fields.Char(string="Model Name")
    for_all = fields.Boolean(string="Users", default=False)
    view_id = fields.Many2one(string="View id", comodel_name="ir.ui.view")

    @api.model
    def get_all_users(self):
        data = self.env['res.users'].search([])
        return [{'id': x.id, 'name': x.login} for x in data]

    @api.model
    def change_fields(self, values):
        records = self.search([("model", "=", values.get("model", False)),
                               ("create_uid", "=", self.env.user.id),
                               ("view_id", '=', values.get("view_id", False))])
        values['fields_show'] = str(values.get('fields_show', {}))
        if records:
            records[0].write(values)
        else:
            self.create(values)
        return True


SUFormDynamic()
