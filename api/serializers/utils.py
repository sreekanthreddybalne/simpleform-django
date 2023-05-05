from .transition import TransitionCREATESerializer

def add_all_transition(qid):
    transition = {
            "from_question": qid,
            "on_value": "*"
    }
    serializer = TransitionCREATESerializer(data=transition)
    if serializer.is_valid():
        serializer.save()
    return