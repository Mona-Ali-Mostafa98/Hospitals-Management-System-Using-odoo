from odoo import models, fields

class Patient(models.Model):
    _name = 'hms.patient' # database model
    _description = 'hms Patient'

    first_name = fields.Char(string='First Name', required=True, placeholder='Enter First Name')
    last_name = fields.Char(string='Last Name', required=True, placeholder='Enter Last Name')
    birth_date = fields.Date(string='Birth Date', placeholder='Enter Birth Date')
    history = fields.Html(string='History', placeholder='Enter History')
    cr_ratio = fields.Float(string='CR Ratio', placeholder='Enter CR Ratio as a float number like 0.00')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string='Blood Type', placeholder='Select Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image', help="Patient's Image")
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.today()
                delta = today - patient.birth_date
                patient.age = delta.days // 365
            else:
                patient.age = 0