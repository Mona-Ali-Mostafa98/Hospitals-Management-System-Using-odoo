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
    age = fields.Integer(string='Age', compute='_compute_age') # store = False not save in db, True mean create column in db, _ means private function
    # lecture 3 - new columns
    email = fields.Char(string='Email', required=True)
    phone_number = fields.Char(string='Phone Number', required=True, unique=True) # don't need to explicitly define in the _sql_constraints attribute
    customer_id = fields.Many2one(comodel_name="res.partner", string='Customer Related', inverse_name="related_patient_id")

    # lecture 2 - relations - new columns
    department_id = fields.Many2one(comodel_name='hms.department', string='Department')
    department_capacity = fields.Integer(related = 'department_id.capacity') # related field take the same type in main table

    doctor_ids = fields.Many2many(comodel_name='hms.doctor', string='Doctors', readonly=True)

    log_history_ids = fields.One2many(comodel_name='hms.log.history', inverse_name='patient_id', string='Log History')

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
    _sql_constraints = [
        ('check_email_uniqueness', 'UNIQUE(email)', 'Email must be unique and this email already exists, use another one.'),
        ('check_valid_email', "CHECK(email ~* '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}')", 'Invalid email format.'),  # validate the email format
        ('check_department_id', 'CHECK(department_id IS NOT NULL)', 'Department ID is required.'),
        # ('check_valid_department_id', 'FOREIGN KEY(department_id) REFERENCES departments(id)', 'Department ID must exist in departments table'), # Ensures referential integrity
        ('check_valid_phone_number', "CHECK(phone_number ~* '^01[0125]\d{8}$')", 'Phone number must start with 010, 011, 012, or 015'),
    ]

    @api.constrains('birth_date')
    def _check_birth_date_before_current_date(self): # "CHECK(birth_date <= CURRENT_DATE)" not working in _sql_constraints
        for rec in self:
            if rec.birth_date and rec.birth_date > fields.Date.today():
                raise ValidationError('Birth date must be before or equal to the current date')

    # ***********************************************************************************************************************
    @api.depends('birth_date') # fire as ajax
    def _compute_age(self):
        for rec in self: # rec is record -> patient
            if rec.birth_date:
                today = fields.Date.today()
                delta = today - rec.birth_date
                rec.age = delta.days // 365
            else:
                rec.age = 0


    # ***********************************************************************************************************************
    @api.onchange('age')
    def _onchange_age(self):
        for rec in self:
            if rec.age < 30 and rec.age != 0:
                rec.pcr = True
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
                    'description': 'State changed to %s' % rec.state
                    # 'description': f"State changed to {dict(self._fields['state'].selection).get(rec.state)}"
                })