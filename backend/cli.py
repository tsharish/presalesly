import typer

from app.db.tenant import (
    create_tenant,
    get_tenants,
    delete_tenant,
)

app = typer.Typer()
tenant_app = typer.Typer()
app.add_typer(tenant_app, name="tenant")


@tenant_app.command()
def create():
    """
    Create a tenant

    The program will be prompt you for the tenant's name, schema and host address
    """
    name = typer.prompt("Tenant name")
    schema = typer.prompt("Name of the tenant's schema")
    host = typer.prompt("Host address of the tenant")
    create_confirm = typer.confirm("Proceed with tenant creation?")

    if not create_confirm:
        typer.echo("Tenant creation canceled")
        raise typer.Exit()

    create_tenant(name=name, schema=schema, host=host)
    typer.echo(f"Tenant created - Name: {name} | Schema: {schema} | Host: {host}")


@tenant_app.command()
def list():
    """Show all the tenants"""
    tenants = get_tenants()
    if tenants is not None:
        if len(tenants) != 0:
            typer.echo("ID | Name | Schema | Host")
            for tenant in tenants:
                typer.echo(f"{tenant.id} | {tenant.name} | {tenant.schema} | {tenant.host}")
        else:
            typer.echo("No tenants found")


@tenant_app.command()
def delete():
    """Delete a tenant"""
    name = typer.prompt("Name of the tenant to be deleted")
    delete_confirm = typer.confirm("Proceed with tenant deletion? This action cannot be reversed.")

    if not delete_confirm:
        typer.echo("Tenant deletion canceled")
        raise typer.Exit()

    try:
        delete_tenant(name=name)
        typer.echo(f"Tenant '{name}' deleted")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app()
