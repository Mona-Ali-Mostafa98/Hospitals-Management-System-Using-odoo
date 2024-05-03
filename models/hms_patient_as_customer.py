from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PatientAsCustomer(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(comodel_name='hms.patient', string='Related Patient')

    vat = fields.Char(required=True)

    _sql_constraints = [
        ('check_patient_id_uniqueness', 'UNIQUE(related_patient_id)', 'only patient related to this record is allowed..............'),
    ]


    # @api.constrains('related_patient_id')
    # def _check_patient_id_uniqueness(self):
    #     for rec in self:
    #         if rec.related_patient_id:
    #             if self.env['res.partner'].search_count([('related_patient_id', '=', rec.related_patient_id.id), ('id', '!=', rec.id)]) > 0:
    #                 raise ValidationError("Only one partner is allowed per patient.")
