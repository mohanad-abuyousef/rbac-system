# Role-Based Access Control (RBAC) in Python

A small command-line program that implements Role-Based Access Control for an "Account" object. Users are assigned to roles, permissions are assigned to roles, and every access decision is made through the user's roles. A user never holds a permission directly.

## Roles and permissions

| Role | Create | View | Update | Delete |
|---|---|---|---|---|
| Admin | yes | yes | yes | yes |
| Manager | - | yes | yes | - |
| Customer | - | yes | - | - |

## How it works

| Step | What happens |
|---|---|
| Assign user to role | The user is stored with the set of roles assigned to them. |
| Assign permission to role | The permission is added to the role's permission set. |
| Access request | The program collects the roles of the acting user and grants the operation only if at least one role holds the required permission. Otherwise it prints `ACCESS DENIED`. |

A user with no role is always denied. A user with several roles receives the union of their permissions.

## Requirements

- Python 3.6 or newer
- No external packages

## Run

```bash
python3 rbac_system.py
```

Menu options: assign a user to a role, assign a permission to a role, show roles, show users, access the Account object (create, view, update, delete), show an access table for all users, exit.

## Example output

```
ACCESS DENIED: 'carol' (Customer) may not Create accounts.
ACCESS GRANTED: 'carol' (Customer) may View accounts.
ACCESS GRANTED: 'bob' (Manager) may Update accounts.
ACCESS DENIED: 'bob' (Manager) may not Delete accounts.
ACCESS GRANTED: 'alice' (Admin) may Delete accounts.
```

## Notes

This is an educational program. Data is kept in memory only and is lost when the program ends. A real system would store users, roles, and permissions in a protected database, authenticate users before checking their roles, and keep an audit log of access decisions.
