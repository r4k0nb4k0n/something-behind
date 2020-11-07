# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hyechoi <hyechoi@student.42seoul.kr>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/11/07 22:19:35 by hyechoi           #+#    #+#              #
#    Updated: 2020/11/08 00:21:07 by hyechoi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

class RequestBodyTodo(BaseModel):
	content: Optional[str] = None
	completed: Optional[bool] = None

db = None
with open('./db.json', 'r+', encoding='utf-8') as f:
	db = json.load(f)

def dbSync():
	with open('./db.json', 'w', encoding='utf-8') as f:
		json.dump(db, f, indent='\t')

def findTodoInDB(todo_id):
	return next(i for i, x in enumerate(db["todos"])\
				if x["id"] == todo_id)

app = FastAPI()

@app.get("/todos/")
async def readTodo():
	try:
		return db
	except Exception as ex:
		return ex

@app.post("/todos/")
async def createTodo(body: RequestBodyTodo):
	try:
		created = {
			"id": len(db["todos"]) + 1,
			"content": body.content,
			"completed": False
		}
		db["todos"] += [ created ]
		dbSync()
		return {
			"success": True,
			"todo": created
		}
	except Exception as ex:
		return {
			"success": False
		}

@app.patch("/todos/{todo_id}")
async def updateTodo(todo_id: int, body: RequestBodyTodo):
	try:
		idx = findTodoInDB(todo_id)
		if body.content is not None:
			db["todos"][idx]["content"] = body.content
		if body.completed is not None:
			db["todos"][idx]["completed"] = body.completed
		dbSync()
		return {
			"success": True,
			"todo": db["todos"][idx]
		}
	except Exception as ex:
		return {
			"success": False
		}

@app.delete("/todos/{todo_id}")
async def deleteTodo(todo_id: int):
	try:
		idx = findTodoInDB(todo_id)
		db["todos"].pop(idx)
		dbSync()
		return {
			"success": True
		}
	except Exception as ex:
		return {
			"success": False
		}
