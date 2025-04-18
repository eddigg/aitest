import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def execute_action(intent: str, action):
    if action:
        try:
            action()
            logging.info(f"Executed intent: {intent}")
            return {"status": "success", "message": f"Command '{intent}' executed"}
        except Exception as e:
            logging.error(f"Error executing {intent}: {e}")
            return {"status": "error", "message": str(e)}
    logging.warning(f"Unknown intent: {intent}")
    return {"status": "unknown_command", "message": "Command not recognized"}"}}}