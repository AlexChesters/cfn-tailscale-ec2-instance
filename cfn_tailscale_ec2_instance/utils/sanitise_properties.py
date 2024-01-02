from aws_lambda_powertools import Logger

logger = Logger()

def sanitise_properties(properties):
    logger.info(f"sanitising: {properties}")

    accept_language = properties.get("AcceptLanguage")
    portfolio_id = properties.get("PortfolioId")
    account_id = properties.get("AccountId")
    organisation_node = properties.get("OrganizationNode")
    share_tag_options = properties.get("ShareTagOptions", "False")
    share_principals = properties.get("SharePrincipals", "False")

    if accept_language and accept_language not in ["jp", "zh"]:
        raise ValueError(f"AcceptLanguage property {accept_language} not valid. Valid options: jp, zh")

    if not portfolio_id:
        raise ValueError("Property PortfolioId not provided")

    if account_id and organisation_node:
        raise ValueError("Cannot specify both AccountId and OrganizationNode")

    if not account_id and not organisation_node:
        raise ValueError("One of AccountId or OrganizationNode must be specified")

    return_dict = {
        "PortfolioId": portfolio_id,
        "ShareTagOptions": share_tag_options.lower() == 'true',
        "SharePrincipals": share_principals.lower() == 'true'
    }

    if accept_language:
        return_dict["AcceptLanguage"] = accept_language

    if organisation_node:
        organisation_node_type = organisation_node.get("Type")
        organisation_node_value = organisation_node.get("Value")

        if not organisation_node_type and not organisation_node_value:
            raise ValueError("Property OrganizationNode is invalid (must contain a Type and Value)")

        return_dict["OrganizationNode"] = {
            "Type": organisation_node_type,
            "Value": organisation_node_value
        }

    logger.info(f"sanitised: {return_dict}")

    return return_dict
