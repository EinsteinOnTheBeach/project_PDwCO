terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "project-rg"
  # ZMIANA: Zaktualizowano region na dostępny w subskrypcji studenckiej
  location = "Poland Central"
}

resource "azurerm_storage_account" "storage" {
  name                     = "iadlabstorage${random_string.random.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # Locally-redundant storage (najtańsza opcja)
}

resource "random_string" "random" {
  length  = 8
  special = false
  upper   = false
}
