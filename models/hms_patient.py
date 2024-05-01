from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient' # database model
    _description = 'hms Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image', help="Patient's Image")
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age') #store=False

    # relations - new columns
    department_id = fields.Many2one(comodel_name='hms.department', string='Department')
    department_capacity = fields.Integer(related = 'department_id.capacity') # related field take the same type in main table

    doctor_ids = fields.Many2many(comodel_name='hms.doctor', string='Doctors', readonly=True)

    log_history_ids = fields.One2many(comodel_name='hms.log_history', inverse_name='patient_id', string='Log History')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')



    """
        ***********************************************************************************************************************
                                method decorators used in Odoo's ORM, define certain behaviors for model methods 
        ***********************************************************************************************************************
    """
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self: # rec is record -> patient
            if rec.birth_date:
                today = fields.Date.today()
                delta = today - rec.birth_date
                rec.age = delta.days // 365
                if rec.age < 30:
                    rec.pcr = True
                else:
                    rec.pcr = False
            else:
                rec.age = 0


    # ***********************************************************************************************************************
    @api.onchange('age')
    def _onchange_age(self):
        for rec in self:
            if rec.pcr and rec.age < 30:
                return { #UserWarning
                    'warning': {'title': 'PCR field has been automatically',
                                'message': 'PCR field has been automatically checked due to age being lower than 30.'}
                }


    # ***********************************************************************************************************************
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and rec.cr_ratio == 0.00: # rec.pcr and rec.cr_ratio == 0.00
                raise ValidationError("CR Ratio field is mandatory when PCR is checked.....")
                # attrs="{'required': [('age', '=', True)]}" -> fix issue when pcr checked cr_ratio accept 0.00


    # ***********************************************************************************************************************
    @api.onchange('department_id')
    def _onchange_department_id(self):
        for rec in self:
            rec.doctor_ids = rec.department_id.doctor_ids


    # ***********************************************************************************************************************
    @api.onchange('state')
    def _onchange_state(self):
        for rec in self:
            if rec.state:
                rec.log_history_ids.create({
                    'patient_id': rec.id,
                    'created_by': self.env.user.id,
                    'date': fields.Date.today(),
                    'description': 'State changed to %s' % rec.state
                    # 'description': f"State changed to {dict(self._fields['state'].selection).get(rec.state)}"
                })