"""
Routes for Server
"""
from api.api import App

print("Router")
# Create an instance of APp with a specific prefix
router_instance = App(prefix="/v1")

# Add routes to the class-based router
router_instance.router.add_api_route(
    "/app/predict", App.predict, methods=["POST"], response_model=dict
)

router_instance.router.add_api_route("/app", App.home, methods=["GET"])
