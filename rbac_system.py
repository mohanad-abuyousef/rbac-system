"""
Role-Based Access Control (RBAC) in Python 3.

Model:
  users  --(assigned to)-->  roles  --(granted)-->  permissions on the "Account" object

A user never receives a permission directly. Every access decision is made by
looking up the user's roles and checking whether any of them holds the
requested permission.

Default roles for the Account object:
  Admin    : Create, View, Update, Delete
  Manager  : View, Update
  Customer : View
"""

CREATE, VIEW, UPDATE, DELETE = "Create", "View", "Update", "Delete"
ALL_PERMISSIONS = [CREATE, VIEW, UPDATE, DELETE]

# role -> set of permissions
role_permissions = {
    "Admin": {CREATE, VIEW, UPDATE, DELETE},
    "Manager": {VIEW, UPDATE},
    "Customer": {VIEW},
}

# user -> set of roles
user_roles = {}

# the protected object: account id -> account holder name
accounts = {1001: "Account Holder A", 1002: "Account Holder B"}


# ---------- RBAC administration ----------

def assign_role(user, role):
    """Assign a user to a role (the user is created if new)."""
    if role not in role_permissions:
        return False, f"Role '{role}' does not exist."
    user_roles.setdefault(user, set())
    if role in user_roles[user]:
        return False, f"User '{user}' already has the role '{role}'."
    user_roles[user].add(role)
    return True, f"User '{user}' assigned to role '{role}'."


def assign_permission(role, permission):
    """Grant a permission to a role."""
    if role not in role_permissions:
        return False, f"Role '{role}' does not exist."
    if permission not in ALL_PERMISSIONS:
        return False, f"Permission '{permission}' does not exist."
    if permission in role_permissions[role]:
        return False, f"Role '{role}' already has the permission '{permission}'."
    role_permissions[role].add(permission)
    return True, f"Permission '{permission}' granted to role '{role}'."


# ---------- access decision ----------

def is_allowed(user, permission):
    """True if at least one of the user's roles holds the permission."""
    for role in user_roles.get(user, set()):
        if permission in role_permissions[role]:
            return True
    return False


def check_access(user, permission):
    """Return (allowed, message) for a user requesting a permission."""
    roles = sorted(user_roles.get(user, set()))
    if not roles:
        return False, f"ACCESS DENIED: '{user}' has no role."
    if is_allowed(user, permission):
        return True, f"ACCESS GRANTED: '{user}' ({', '.join(roles)}) may {permission} accounts."
    return False, f"ACCESS DENIED: '{user}' ({', '.join(roles)}) may not {permission} accounts."


# ---------- operations on the Account object ----------

def create_account(user, acc_id, holder):
    ok, msg = check_access(user, CREATE)
    print("  " + msg)
    if ok:
        if acc_id in accounts:
            print(f"  Account {acc_id} already exists.")
        else:
            accounts[acc_id] = holder
            print(f"  Account {acc_id} created for {holder}.")


def view_accounts(user):
    ok, msg = check_access(user, VIEW)
    print("  " + msg)
    if ok:
        for acc_id, holder in accounts.items():
            print(f"    {acc_id} : {holder}")


def update_account(user, acc_id, holder):
    ok, msg = check_access(user, UPDATE)
    print("  " + msg)
    if ok:
        if acc_id in accounts:
            accounts[acc_id] = holder
            print(f"  Account {acc_id} updated.")
        else:
            print(f"  Account {acc_id} not found.")


def delete_account(user, acc_id):
    ok, msg = check_access(user, DELETE)
    print("  " + msg)
    if ok:
        if acc_id in accounts:
            del accounts[acc_id]
            print(f"  Account {acc_id} deleted.")
        else:
            print(f"  Account {acc_id} not found.")


# ---------- reports ----------

def show_roles():
    print("\n  Role        Create  View  Update  Delete")
    print("  " + "-" * 44)
    for role, perms in role_permissions.items():
        marks = ["yes" if p in perms else "-" for p in ALL_PERMISSIONS]
        print(f"  {role:<10}  {marks[0]:<6}  {marks[1]:<4}  {marks[2]:<6}  {marks[3]}")


def show_users():
    if not user_roles:
        print("  (no users yet)")
        return
    print("\n  User        Roles")
    print("  " + "-" * 30)
    for user, roles in user_roles.items():
        print(f"  {user:<10}  {', '.join(sorted(roles)) if roles else '-'}")


def show_access_table():
    if not user_roles:
        print("  (no users yet)")
        return
    print("\n  User        Create   View     Update   Delete")
    print("  " + "-" * 52)
    for user in user_roles:
        cells = ["ALLOWED" if is_allowed(user, p) else "denied" for p in ALL_PERMISSIONS]
        print(f"  {user:<10}  {cells[0]:<7}  {cells[1]:<7}  {cells[2]:<7}  {cells[3]}")


# ---------- user interface ----------

def read_number(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("  Invalid number.")
        return None


def account_menu():
    user = input("  Acting user : ").strip()
    print("  1) Create   2) View   3) Update   4) Delete")
    choice = input("  Operation   : ").strip()
    operations = {"1": CREATE, "2": VIEW, "3": UPDATE, "4": DELETE}
    if choice not in operations:
        print("  Invalid operation.")
        return
    # The access decision is made before any further input is requested.
    if not is_allowed(user, operations[choice]):
        print("  " + check_access(user, operations[choice])[1])
        return
    if choice == "1":
        acc_id = read_number("  New account number : ")
        if acc_id is not None:
            create_account(user, acc_id, input("  Account holder     : ").strip())
    elif choice == "2":
        view_accounts(user)
    elif choice == "3":
        acc_id = read_number("  Account number  : ")
        if acc_id is not None:
            update_account(user, acc_id, input("  New holder name : ").strip())
    elif choice == "4":
        acc_id = read_number("  Account number : ")
        if acc_id is not None:
            delete_account(user, acc_id)


def main():
    print("=" * 60)
    print(" Role-Based Access Control (RBAC) System")
    print("=" * 60)
    while True:
        print("\n1) Assign user to role      2) Assign permission to role")
        print("3) Show roles               4) Show users")
        print("5) Access the Account       6) Show access table")
        print("7) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            user = input("  User name : ").strip()
            role = input("  Role (Admin/Manager/Customer) : ").strip().capitalize()
            print("  " + assign_role(user, role)[1])
        elif choice == "2":
            role = input("  Role : ").strip().capitalize()
            perm = input("  Permission (Create/View/Update/Delete) : ").strip().capitalize()
            print("  " + assign_permission(role, perm)[1])
        elif choice == "3":
            show_roles()
        elif choice == "4":
            show_users()
        elif choice == "5":
            account_menu()
        elif choice == "6":
            show_access_table()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
