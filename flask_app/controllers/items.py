from flask_app.models.user import User
from flask_app.models.item import Item
from flask import flash
from flask_app import app
from flask import Flask, redirect, render_template, request, session
from datetime import datetime
dateFormat = "%m/%d/%Y"

@app.route('/item/add_item')
def add_item_form():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : session['user_id']
    }
    
    return render_template('add_item.html')

@app.route('/item/create', methods=['POST'])
def create_item():
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Item.item_validator(request.form):
        return redirect('/item/add_item')
    
            
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'qty' : request.form['qty'],
        'date_requested' : request.form['date_requested'],
        'user_id' : session['user_id'] 
    }
    
    Item.create_item(data)
    return redirect('/dashboard')
    
   

@app.route('/item/edit_item/<int:item_id>')
def edit_item(item_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : item_id
    }    
    return render_template("edit_item.html", item = Item.get_one(data))

@app.route('/item/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    valid = Item.item_validator(request.form)
    if valid:
        Item.update_item(request.form)
        return redirect('/dashboard')
    
    return redirect(f"/item/edit_item/{item_id}")

@app.route('/item/delete_item/<int:item_id>')
def delete_item(item_id):    
    if 'user_id' not in session:
        return redirect('/logout')    
    data = {
        'id' : item_id
    }
    Item.delete_item(data)
    return redirect('/dashboard')

@app.route('/item/delete_all')
def delete_all():
    if 'user_id' not in session:
        return redirect('/logout')
    
    Item.delete_all()
    return redirect('/dashboard')
    

@app.route('/item/<int:item_id>')
def display_item(item_id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id' : item_id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('view_item.html', item = Item.get_by_id(data), date = dateFormat)



