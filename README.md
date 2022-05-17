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

[`bcli` is available on PyPI](https://pypi.org/project/bigcommerce-cli/). Use the command `pip install bigcommerce-cli` for easy installation. 

# Getting Started

Use the `bcli settings add-store` command to save a store for `bcli` to use later. Then, use
the `bcli settings active-store` command to select which saved store should be used for your management commands.

Once `bcli` has an active store, you can make DELETE, GET, POST, and PUT commands to manage resources on that store.

# Supported Commands

Delete a BigCommerce resource.

- `bcli delete products <product id>`
- `bcli delete customers <customer id>`

Get a list of BigCommerce resources.

- `bcli get products`
- `bcli get product-variants <product id>`
- `bcli get customers`

Get details about a BigCommerce resource.

- `bcli get products <product id>`
- `bcli get product-variants <product id> <variant id>`
- `bcli get customers <customer id>`

Update a BigCommerce resource.

- `bcli put products <product id>`
- `bcli put product-variants <product id> <variant id>`
- `bcli put customers <customer id>`

Create a BigCommerce resource.

- `bcli post products`
- `bcli post customers`

Manage `bcli` settings.

- `bcli settings delete-store`
- `bcli settings list-stores`
- `bcli settings add-store`
- `bcli settings active-store`
