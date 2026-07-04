# utils.py

def normalize_text(text: str) -> str:
    """
    Normalizza il testo vocale:
    - lowercase
    - strip
    - rimuove spazi multipli
    """
    if not text:
        return ""

    return " ".join(text.lower().strip().split())


# ==========================================
# FUNZIONI DINAMICHE
# ==========================================

def build_auto_activate_func_name(
    checklist_name: str,
    auto_activate_value: str
) -> str:
    """
    auto_activate_pre_flight_func_beacon_on
    """
    return f"auto_activate_{checklist_name}_func_{auto_activate_value}"


def build_final_function_name(
    checklist_name: str,
    step_number: int,
    result_type: str,
    func_value: str
) -> str:
    """
    pre_flight_step1_error_func_battery
    """
    return (
        f"{checklist_name}_"
        f"step{step_number}_"
        f"{result_type}_"
        f"func_{func_value}"
    )


# ==========================================
# CHECKLIST / STEP HELPERS
# ==========================================

def find_step(sequence: list, step_number: int) -> dict | None:
    """
    Trova uno step nella sequence.
    """
    for step in sequence:
        if step.get("step") == step_number:
            return step
    return None


def is_valid_answer(answer: str, answers_list: list) -> bool:
    """
    Verifica se una risposta vocale matcha una lista
    """
    return normalize_text(answer) in [
        normalize_text(a) for a in answers_list
    ]


# ==========================================
# STATO CHECKLIST
# ==========================================

def can_activate_checklist(checklist: dict, any_active: bool) -> bool:
    """
    Regole base di attivazione
    """
    if checklist.get("activated"):
        return False

    if checklist.get("is_active"):
        return False

    if not checklist.get("can_be_automated", True):
        return False

    if any_active:
        return False

    return True


def reset_checklist_state(checklist: dict):
    """
    Reset di sicurezza (se serve)
    """
    checklist["is_active"] = False
    checklist["activated"] = False
    checklist["can_be_automated"] = True