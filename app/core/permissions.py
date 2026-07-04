from enum import Enum

class UserRole(str, Enum):
    Admin = 'Admin'
    Treasurer = 'Treasurer'
    Secretary = 'Secretary'
    Chairperson = 'Chairperson'
    Member = 'Member'

class UserStatus(str, Enum):
    Active = 'Active'
    Inactive = 'Inactive'
