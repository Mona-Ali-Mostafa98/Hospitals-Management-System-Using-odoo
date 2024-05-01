from odoo import models, fields, api

class Patient(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Image', help="Doctor's Image")

    department_id = fields.Many2one(comodel_name='hms.department', string='Department')
