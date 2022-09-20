# BigCommerce CLI

`bcli` is BigCommerce store management on the command line. It brings the most commonly used store management tools to
the terminal for quick actions and multi-storefront workflows. `bcli` was written to help tech savvy store managers save
time by ditching BigCommerce's browser based admin UI.

```
      :::::::::   ::::::::  :::        ::::::::::: 
     :+:    :+: :+:    :+: :+:            :+:      
    +:+    +:+ +:+        +:+            +:+       
   +#++:++#+  +#+        +#+            +#+        
  +#+    +#+ +#+        +#+            +#+         
 #+#    #+# #+#    #+# #+#            #+#          
#########   ########  ########## ###########       
```

# Installation

[`bcli` is available on PyPI](https://pypi.org/project/bigcommerce-cli/). Use the command `pip install bigcommerce-cli`
for easy installation.

# Getting Started

Use the `bcli settings add-store` command to save a store for `bcli` to use later. Then, use
the `bcli settings active-store` command to select which saved store should be used for your management commands.

Once `bcli` has an active store, you can make DELETE, GET, POST, and PUT commands to manage resources on that store.

# Supported Commands

Delete a BigCommerce resource.

- `bcli delete customers <customer id>`
- `bcli delete products <product id>`
- `bcli delete webhooks <webhook id>`

Get a list of BigCommerce resources.

- `bcli get customers`
- `bcli get order-products <order id>`
- `bcli get orders`
- `bcli get product-variants <product id>`
- `bcli get products`
- `bcli get webhooks`

Get details about a BigCommerce resource.

- `bcli get customers <customer id>`
- `bcli get order-products <order id> <order product id>`
- `bcli get orders <order id>`
- `bcli get product-variants <product id> <variant id>`
- `bcli get products <product id>`
- `bcli get webhooks <webhook id>`

Update a BigCommerce resource.

- `bcli put customers <customer id>`
- `bcli put product-variants <product id> <variant id>`
- `bcli put products <product id>`
- `bcli put webhooks <webhook id>`

Create a BigCommerce resource.

- `bcli post customers`
- `bcli post products`
- `bcli post webhooks`

Manage `bcli` settings.

- `bcli settings delete-store`
- `bcli settings list-stores`
- `bcli settings add-store`
- `bcli settings active-store`
