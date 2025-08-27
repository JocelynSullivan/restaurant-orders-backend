from fastapi import FastAPI

from routers import customer, menu, order, reports

app = FastAPI()

app.include_router(customer.router, tags=["Customer"])
app.include_router(menu.router, tags=["Menu"])
app.include_router(order.router, tags=["Order"])
app.include_router(reports.router, tags=["Reports"])
