from openerp.models import BaseModel, AbstractModel
from openerp import api
from openerp import SUPERUSER_ID
import json
from lxml import etree

_fields_view_get = AbstractModel.fields_view_get


@api.model
def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    res = _fields_view_get(self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    # if view_type in ['list', 'tree'] and (odoo.SUPERUSER_ID ==
    # self.env.user.id or self.env.ref('su_dynamic_listview.group_show_field') in self.env.user.groups_id):
    if view_type in ['form'] and 'form.dynamic' in self.env.registry.models:
        form_dynamic_obj = self.env['form.dynamic']
        shf_obj = form_dynamic_obj.search([('model', '=', self._name),
                                           ('view_id', '=', res.get('view_id', False)),
                                           ('create_uid', '=', SUPERUSER_ID)])
        if shf_obj:
            shf_obj = shf_obj if shf_obj.for_all else form_dynamic_obj.search([('model', '=', self._name),
                                                                             ('view_id', '=', res.get('view_id', False)),
                                                                             ('create_uid', '=', self.env.user.id)])
        else:
            shf_obj = form_dynamic_obj.search([('model', '=', self._name),
                                               ('view_id', '=', res.get('view_id', False)),
                                               ('create_uid', '=', self.env.user.id)])

        def check_ok(d):
            if d == "False" or d is False or d == "false" or d == '0' or d == 0:
                return 0
            if d == "True" or d is True or d == "true" or d == '1' or d == 1:
                return 1
            if isinstance(d, basestring) and d.find("[[") >= 0:
                pass
            return d

        if shf_obj:
            doc = etree.XML(res['arch'])
            fields_show = eval(shf_obj[0].fields_show)
            for _field_name in fields_show:
                f = doc.xpath("//field[@name='%s']" % _field_name['name'])
                for _f in f:
                    if 'name' in _f.attrib:
                        attrs = _f.get("attrs") or '{}'
                        modifiers = _f.get("modifiers") or '{}'
                        if modifiers:
                            modifiers = modifiers.replace("true", '1').replace("false", '0')
                            modifiers = eval(modifiers)
                            modifiers["string"] = check_ok(_field_name['string'])
                            modifiers["invisible"] = check_ok(_field_name['invisible'])
                            modifiers["readonly"] = check_ok(_field_name['readonly'])
                            modifiers["required"] = check_ok(_field_name['required'])
                            _f.set("modifiers", json.dumps(modifiers))
                        if attrs:
                            attrs = attrs.replace("true", '1').replace("false", '0')
                            attrs = eval(attrs)
                            attrs["string"] = check_ok(_field_name['string'])
                            attrs["invisible"] = check_ok(_field_name['invisible'])
                            attrs["readonly"] = check_ok(_field_name['readonly'])
                            attrs["required"] = check_ok(_field_name['required'])
                            _f.set("attrs", json.dumps(attrs))
                        _f.set("string", str(_field_name['string']))
                        field = res['fields'][_field_name['name']]
                        if 'tree' in field['views'] and 'line' in _field_name:
                            line_doc = etree.XML(field['views']['tree']['arch'])
                            line_field = _field_name['line']
                            for lf in line_field:
                                _lf = line_doc.xpath("//field[@name='%s']" % lf['name'])
                                for _lf_ in _lf:
                                    if 'name' in _lf_.attrib:
                                        _attrs = _lf_.get("attrs") or '{}'
                                        _modifiers = _lf_.get("modifiers") or '{}'
                                        if _modifiers:
                                            _modifiers = _modifiers.replace("true", '1').replace("false", '0')
                                            _modifiers = eval(_modifiers)
                                            _modifiers["string"] = check_ok(lf['string'])
                                            _modifiers["invisible"] = check_ok(lf['invisible'])
                                            _modifiers["readonly"] = check_ok(lf['readonly'])
                                            _modifiers["required"] = check_ok(lf['required'])
                                            _modifiers["tree_invisible"] = check_ok(lf['invisible'])
                                            _lf_.set("modifiers", json.dumps(_modifiers))
                                        _lf_.set("string", str(check_ok(lf['string'])))
                                        _lf_.set("required", str(check_ok(lf['required'])))
                                        _lf_.set("invisible", str(check_ok(lf['invisible'])))
                                        _lf_.set("readonly", str(check_ok(lf['readonly'])))
                            field['views']['tree']['arch'] = etree.tostring(line_doc)
            if shf_obj.for_all:
                for f in doc.xpath("//form"):
                    f.set("apply_for_all", "1")
            res['arch'] = etree.tostring(doc)
    return res


AbstractModel.fields_view_get = fields_view_get
