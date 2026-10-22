"""Manage gym membership registration, renewals, and roster exports."""

import hashlib
import secrets

MEMBERS = {
    "M01": {
        "name": "Alex",
        "plan": "Gold",
        "months_left": 6,
        "fee": 600.0,
    },
    "M02": {
        "name": "Brooke",
        "plan": "Silver",
        "months_left": 1,
        "fee": 350.0,
    },
    "M03": {
        "name": "Chris",
        "plan": "Platinum",
        "months_left": 12,
        "fee": 1000.0,
    },
}


def register_member(m_id, name, plan, months, member_log=None):
    """Register a new member if the ID and membership duration are valid."""
    if m_id in MEMBERS or months <= 0:
        return False

    MEMBERS[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }

    if member_log is not None:
        member_log.append(f"Registered {m_id} for {months} months")

    return True


def cancel_membership(m_id):
    """Cancel a membership and report whether the member existed."""
    if m_id not in MEMBERS:
        return False

    del MEMBERS[m_id]
    return True


def check_membership_status(m_id):
    """Return whether a member exists and has time remaining."""
    member = MEMBERS.get(m_id)
    return member is not None and member["months_left"] > 0


def calculate_renewal_rate(m_id, discount_percent):
    """Calculate the renewal fee after applying a percentage discount."""
    if m_id not in MEMBERS:
        raise ValueError(f"Unknown member ID: {m_id}")

    if not isinstance(discount_percent, (int, float)):
        raise TypeError("Discount must be a number.")

    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100.")

    base_fee = MEMBERS[m_id]["fee"]
    return round(base_fee * (1 - discount_percent / 100), 2)


def generate_member_hash(m_id):
    """Generate a SHA-256 digest for a member ID."""
    return hashlib.sha256(m_id.encode("utf-8")).hexdigest()


def generate_locker_pin():
    """Generate a four-digit locker PIN using a secure random generator."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    """Export the current member roster to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(MEMBERS))

    print(f"Roster exported to: {filename}")


def get_active_summary(member_records):
    """Return the number of members whose memberships are still active."""
    return sum(
        details["months_left"] > 0
        for details in member_records.values()
    )


def main():
    """Demonstrate the gym membership system."""
    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")

    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", 15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())

    export_member_roster()
    print("Active count:", get_active_summary(MEMBERS))


if __name__ == "__main__":
    main()
