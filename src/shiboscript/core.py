"""Core ShiboScript interpreter implementation"""
import re
from collections import namedtuple
from PIL import Image
import math
import sys
import urllib.request
import urllib.parse
import base64
import hashlib
import subprocess
import os
import random
import string
import json
import time
import datetime
import sqlite3

# Database ORM Implementation
class Database:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.models = {}
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute(self, query, params=None):
        if not self.connection:
            self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Database query failed: {str(e)}", query)
    
    def create_table(self, table_name, columns):
        columns_def = ", ".join([f"{name} {type_def}" for name, type_def in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        return self.execute(query)
    
    def insert(self, table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute(query, values)
    
    def select(self, table_name, conditions=None, columns="*"):
        query = f"SELECT {columns} FROM {table_name}"
        params = []
        if conditions:
            where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
            query += f" WHERE {where_clause}"
            params = list(conditions.values())
        return self.execute(query, params)
    
    def update(self, table_name, data, conditions):
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        values = list(data.values()) + list(conditions.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        return self.execute(query, values)
    
    def delete(self, table_name, conditions):
        where_clause = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        params = list(conditions.values())
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        return self.execute(query, params)

class Model:
    def __init__(self, db, table_name, schema):
        self.db = db
        self.table_name = table_name
        self.schema = schema
        self.db.create_table(table_name, schema)
    
    def create(self, data):
        self.db.insert(self.table_name, data)
        return self.find_one(data)
    
    def find(self, conditions=None):
        results = self.db.select(self.table_name, conditions)
        return [dict(zip(self.schema.keys(), row)) for row in results]
    
    def find_one(self, conditions):
        results = self.find(conditions)
        return results[0] if results else None
    
    def update(self, data, conditions):
        return self.db.update(self.table_name, data, conditions)
    
    def delete(self, conditions):
        return self.db.delete(self.table_name, conditions)
    
    def all(self):
        return self.find()

# Query Builder
class QueryBuilder:
    def __init__(self, db):
        self.db = db
        self.reset()
    
    def reset(self):
        self.table = None
        self.columns = "*"
        self.conditions = []
        self.order_by = None
        self.limit = None
        self.joins = []
    
    def from_table(self, table_name):
        self.table = table_name
        return self
    
    def select(self, columns):
        self.columns = ", ".join(columns) if isinstance(columns, list) else columns
        return self
    
    def where(self, column, operator, value):
        self.conditions.append(f"{column} {operator} ?")
        return self
    
    def order_by(self, column, direction="ASC"):
        self.order_by = f"{column} {direction}"
        return self
    
    def limit(self, count):
        self.limit = count
        return self
    
    def join(self, table, condition):
        self.joins.append(f"JOIN {table} ON {condition}")
        return self
    
    def execute(self):
        if not self.table:
            raise ValidationError("No table specified for query")
        
        query = f"SELECT {self.columns} FROM {self.table}"
        
        # Add joins
        for join in self.joins:
            query += f" {join}"
        
        # Add conditions
        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
        
        # Add ordering
        if self.order_by:
            query += f" ORDER BY {self.order_by}"
        
        # Add limit
        if self.limit:
            query += f" LIMIT {self.limit}"
        
        return self.db.execute(query)

# Database utilities
def create_database(db_path=":memory:"):
    return Database(db_path).connect()

def create_model(db, table_name, schema):
    return Model(db, table_name, schema)

def query_builder(db):
    return QueryBuilder(db)

# Module System Implementation
class Module:
    def __init__(self, name, exports=None):
        self.name = name
        self.exports = exports or {}
        self.loaded = False
    
    def add_export(self, name, value):
        self.exports[name] = value
    
    def get_export(self, name):
        return self.exports.get(name)
    
    def get_all_exports(self):
        return self.exports.copy()

class ModuleLoader:
    def __init__(self):
        self.modules = {}
        self.module_paths = [".", "./modules", "./lib"]
    
    def load_module(self, module_name):
        if module_name in self.modules:
            return self.modules[module_name]
        
        # Try to load from file
        module_path = self.find_module_file(module_name)
        if module_path:
            return self.load_from_file(module_name, module_path)
        
        # Create built-in module
        return self.create_builtin_module(module_name)
    
    def find_module_file(self, module_name):
        import os
        for path in self.module_paths:
            file_path = os.path.join(path, module_name + ".shibo")
            if os.path.exists(file_path):
                return file_path
        return None
    
    def load_from_file(self, module_name, file_path):
        # This would load and execute the module file
        # For now, we'll create a placeholder
        module = Module(module_name)
        # In a real implementation, we would parse and execute the file
        self.modules[module_name] = module
        return module
    
    def create_builtin_module(self, module_name):
        module = Module(module_name)
        
        # Add built-in modules
        if module_name == "math":
            module.add_export("PI", 3.14159)
            module.add_export("sqrt", lambda x: x ** 0.5)
            module.add_export("pow", lambda x, y: x ** y)
        elif module_name == "utils":
            module.add_export("is_even", lambda x: x % 2 == 0)
            module.add_export("is_odd", lambda x: x % 2 == 1)
            module.add_export("clamp", lambda value, min_val, max_val: max(min_val, min(max_val, value)))
        elif module_name == "string":
            module.add_export("capitalize", lambda s: s[0].upper() + s[1:].lower() if s else s)
            module.add_export("reverse", lambda s: s[::-1])
            module.add_export("is_palindrome", lambda s: s.lower() == s.lower()[::-1])
        
        self.modules[module_name] = module
        return module
    
    def import_module(self, module_name):
        module = self.load_module(module_name)
        return module.get_all_exports()
    
    def export_from_module(self, module_name, export_name, value):
        if module_name not in self.modules:
            self.modules[module_name] = Module(module_name)
        self.modules[module_name].add_export(export_name, value)

# Global module loader
_module_loader = ModuleLoader()

# Module system functions
def import_module(module_name):
    return _module_loader.import_module(module_name)

def export_to_module(module_name, export_name, value):
    _module_loader.export_from_module(module_name, export_name, value)

def create_module(name):
    return Module(name)

# Structured Logging and Monitoring
class Logger:
    def __init__(self, name="ShiboScript", level="INFO"):
        self.name = name
        self.level = level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}
        self.level_num = self.levels.get(level, 1)
        self.logs = []
    
    def _should_log(self, log_level):
        return self.levels.get(log_level, 1) >= self.level_num
    
    def _format_log(self, level, message, **kwargs):
        import json
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "logger": self.name,
            "message": message,
            "data": kwargs
        }
        return json.dumps(log_entry)
    
    def debug(self, message, **kwargs):
        if self._should_log("DEBUG"):
            log_entry = self._format_log("DEBUG", message, **kwargs)
            self.logs.append(log_entry)
            print(f"DEBUG: {message}")
            return log_entry
    
    def info(self, message, **kwargs):
        if self._should_log("INFO"):
            log_entry = self._format_log("INFO", message, **kwargs)
            self.logs.append(log_entry)
            print(f"INFO: {message}")
            return log_entry
    
    def warn(self, message, **kwargs):
        if self._should_log("WARN"):
            log_entry = self._format_log("WARN", message, **kwargs)
            self.logs.append(log_entry)
            print(f"WARN: {message}")
            return log_entry
    
    def error(self, message, **kwargs):
        if self._should_log("ERROR"):
            log_entry = self._format_log("ERROR", message, **kwargs)
            self.logs.append(log_entry)
            print(f"ERROR: {message}")
            return log_entry
    
    def fatal(self, message, **kwargs):
        log_entry = self._format_log("FATAL", message, **kwargs)
        self.logs.append(log_entry)
        print(f"FATAL: {message}")
        return log_entry
    
    def get_logs(self, level=None):
        if level:
            level_num = self.levels.get(level, 0)
            return [log for log in self.logs if self.levels.get(eval(log).get("level", "INFO"), 1) >= level_num]
        return self.logs.copy()
    
    def clear_logs(self):
        self.logs.clear()
    
    def save_logs(self, filename):
        with open(filename, "w") as f:
            for log in self.logs:
                f.write(log + "\n")

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        self.timers = {}
    
    def increment(self, metric_name, value=1):
        if metric_name not in self.metrics:
            self.metrics[metric_name] = 0
        self.metrics[metric_name] += value
        return self.metrics[metric_name]
    
    def set(self, metric_name, value):
        self.metrics[metric_name] = value
        return value
    
    def get(self, metric_name, default=0):
        return self.metrics.get(metric_name, default)
    
    def start_timer(self, timer_name):
        import time
        self.timers[timer_name] = time.time()
    
    def stop_timer(self, timer_name):
        import time
        if timer_name in self.timers:
            elapsed = time.time() - self.timers[timer_name]
            self.increment(f"{timer_name}_duration", elapsed)
            self.increment(f"{timer_name}_count")
            del self.timers[timer_name]
            return elapsed
        return None
    
    def get_all_metrics(self):
        return self.metrics.copy()
    
    def reset_metrics(self):
        self.metrics.clear()

class HealthChecker:
    def __init__(self):
        self.checks = {}
        self.results = {}
    
    def add_check(self, name, check_func):
        self.checks[name] = check_func
    
    def run_check(self, name):
        if name in self.checks:
            try:
                result = self.checks[name]()
                self.results[name] = {"status": "healthy", "result": result}
                return True
            except Exception as e:
                self.results[name] = {"status": "unhealthy", "error": str(e)}
                return False
        return False
    
    def run_all_checks(self):
        results = {}
        for name in self.checks:
            results[name] = self.run_check(name)
        return results
    
    def get_status(self):
        healthy = sum(1 for result in self.results.values() if result["status"] == "healthy")
        total = len(self.results)
        return {
            "healthy": healthy,
            "total": total,
            "percentage": (healthy / total * 100) if total > 0 else 0,
            "details": self.results.copy()
        }

# Global logging and monitoring instances
_default_logger = Logger("ShiboScript")
_metrics_collector = MetricsCollector()
_health_checker = HealthChecker()

# Logging functions
def create_logger(name, level="INFO"):
    return Logger(name, level)

def log_debug(message, **kwargs):
    return _default_logger.debug(message, **kwargs)

def log_info(message, **kwargs):
    return _default_logger.info(message, **kwargs)

def log_warn(message, **kwargs):
    return _default_logger.warn(message, **kwargs)

def log_error(message, **kwargs):
    return _default_logger.error(message, **kwargs)

def log_fatal(message, **kwargs):
    return _default_logger.fatal(message, **kwargs)

def get_logs(level=None):
    return _default_logger.get_logs(level)

# Metrics functions
def metric_increment(name, value=1):
    return _metrics_collector.increment(name, value)

def metric_set(name, value):
    return _metrics_collector.set(name, value)

def metric_get(name, default=0):
    return _metrics_collector.get(name, default)

def start_timer(name):
    _metrics_collector.start_timer(name)

def stop_timer(name):
    return _metrics_collector.stop_timer(name)

def get_metrics():
    return _metrics_collector.get_all_metrics()

def reset_metrics():
    _metrics_collector.reset_metrics()

# Health check functions
def add_health_check(name, check_func):
    _health_checker.add_check(name, check_func)

def run_health_check(name):
    return _health_checker.run_check(name)

def run_all_health_checks():
    return _health_checker.run_all_checks()

def get_health_status():
    return _health_checker.get_status()

# Enhanced Error Handling

class ShiboException(Exception):
    def __init__(self, message, error_type="RuntimeError", line=None, file=None):
        self.message = message
        self.error_type = error_type
        self.line = line
        self.file = file
        self.stack_trace = []
        super().__init__(self.format_message())
    
    def format_message(self):
        msg = f"{self.error_type}: {self.message}"
        if self.line is not None:
            msg += f" at line {self.line}"
        if self.file is not None:
            msg += f" in {self.file}"
        return msg
    
    def add_stack_frame(self, function, line):
        self.stack_trace.append((function, line))
    
    def print_stack_trace(self):
        if self.stack_trace:
            print("Stack trace:")
            for i, (func, line) in enumerate(reversed(self.stack_trace)):
                print(f"  {i+1}. {func} at line {line}")

class ValidationError(ShiboException):
    def __init__(self, message, field=None):
        super().__init__(message, "ValidationError")
        self.field = field

class NetworkError(ShiboException):
    def __init__(self, message, url=None):
        super().__init__(message, "NetworkError")
        self.url = url

class DatabaseError(ShiboException):
    def __init__(self, message, query=None):
        super().__init__(message, "DatabaseError")
        self.query = query

class FileNotFoundError(ShiboException):
    def __init__(self, message, path=None):
        super().__init__(message, "FileNotFoundError")
        self.path = path

class PermissionError(ShiboException):
    def __init__(self, message, operation=None):
        super().__init__(message, "PermissionError")
        self.operation = operation

# Enhanced error handling utilities
def try_catch(try_func, catch_func=None, finally_func=None):
    try:
        result = try_func()
        if finally_func:
            finally_func()
        return result
    except Exception as e:
        if catch_func:
            catch_func(e)
        if finally_func:
            finally_func()
        raise

def assert_condition(condition, message="Assertion failed"):
    if not condition:
        raise ValidationError(message)

def validate_type(value, expected_type, field_name=None):
    if not isinstance(value, expected_type):
        field_msg = f" for field '{field_name}'" if field_name else ""
        raise ValidationError(f"Expected {expected_type.__name__}, got {type(value).__name__}{field_msg}")

def validate_range(value, min_val=None, max_val=None, field_name=None):
    if min_val is not None and value < min_val:
        raise ValidationError(f"Value {value} is less than minimum {min_val}{'' if not field_name else f' for {field_name}'}")
    if max_val is not None and value > max_val:
        raise ValidationError(f"Value {value} is greater than maximum {max_val}{'' if not field_name else f' for {field_name}'}")

# Advanced data structures

class Set:
    def __init__(self, items=None):
        self._items = {}
        if items:
            for item in items:
                self._items[item] = True
    
    def add(self, item):
        self._items[item] = True
        return self
    
    def remove(self, item):
        if item in self._items:
            del self._items[item]
        return self
    
    def contains(self, item):
        return item in self._items
    
    def size(self):
        return len(self._items)
    
    def to_list(self):
        return list(self._items.keys())
    
    def union(self, other_set):
        new_set = Set(self.to_list())
        for item in other_set.to_list():
            new_set.add(item)
        return new_set
    
    def intersection(self, other_set):
        new_set = Set()
        for item in self.to_list():
            if other_set.contains(item):
                new_set.add(item)
        return new_set
    
    def difference(self, other_set):
        new_set = Set()
        for item in self.to_list():
            if not other_set.contains(item):
                new_set.add(item)
        return new_set

class Queue:
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        self._items.append(item)
        return self
    
    def dequeue(self):
        if self._items:
            return self._items.pop(0)
        return None
    
    def front(self):
        return self._items[0] if self._items else None
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def to_list(self):
        return self._items[:]

class Stack:
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
        return self
    
    def pop(self):
        if self._items:
            return self._items.pop()
        return None
    
    def peek(self):
        return self._items[-1] if self._items else None
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def to_list(self):
        return self._items[:]

class PriorityQueue:
    def __init__(self):
        self._items = []
    
    def enqueue(self, item, priority):
        self._items.append((priority, item))
        self._items.sort(key=lambda x: x[0])
        return self
    
    def dequeue(self):
        if self._items:
            return self._items.pop(0)[1]
        return None
    
    def peek(self):
        return self._items[0][1] if self._items else None
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)

# Functional programming utilities
def map_func(func, iterable):
    return [func(item) for item in iterable]

def filter_func(func, iterable):
    return [item for item in iterable if func(item)]

def reduce_func(func, iterable, initial=None):
    if initial is None:
        result = iterable[0]
        items = iterable[1:]
    else:
        result = initial
        items = iterable
    
    for item in items:
        result = func(result, item)
    return result

def compose(*functions):
    def composed_function(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed_function

def partial(func, *args, **kwargs):
    def partial_function(*more_args, **more_kwargs):
        all_args = args + more_args
        all_kwargs = {**kwargs, **more_kwargs}
        return func(*all_args, **all_kwargs)
    return partial_function

# Data structure algorithms
def _binary_search(lst, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return _binary_search(lst, target, mid + 1, right)
    else:
        return _binary_search(lst, target, left, mid - 1)

def _quick_sort(lst):
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return _quick_sort(left) + middle + _quick_sort(right)

def _merge_sort(lst):
    if len(lst) <= 1:
        return lst
    
    mid = len(lst) // 2
    left = _merge_sort(lst[:mid])
    right = _merge_sort(lst[mid:])
    
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Advanced utilities
def _deep_copy(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, list):
        return [_deep_copy(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _deep_copy(value) for key, value in obj.items()}
    elif isinstance(obj, (Set, Queue, Stack, PriorityQueue)):
        return obj.__class__(obj.to_list())
    else:
        return obj

def _flatten_list(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(_flatten_list(item))
        else:
            result.append(item)
    return result

def _group_by(lst, key_func):
    groups = {}
    for item in lst:
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def _debounce(func, delay):
    import time
    last_call = [0]
    def debounced_func(*args, **kwargs):
        now = time.time()
        if now - last_call[0] >= delay:
            last_call[0] = now
            return func(*args, **kwargs)
    return debounced_func

def _memoize(func):
    cache = {}
    def memoized_func(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func

# Async/Await Support
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

# Event Loop Implementation
class EventLoop:
    def __init__(self):
        self.tasks = []
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def create_task(self, coro):
        task = Task(coro, self)
        self.tasks.append(task)
        return task
    
    def run_until_complete(self):
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                task.step()
                if not task.done:
                    self.tasks.append(task)
            except Exception as e:
                print(f"Task error: {e}")
                task.done = True
                task.result = e
    
    def run_in_thread(self, func, *args, **kwargs):
        future = self.executor.submit(func, *args, **kwargs)
        return future

class Task:
    def __init__(self, coro, loop):
        self.coro = coro
        self.loop = loop
        self.done = False
        self.result = None
        self.exception = None
    
    def step(self):
        try:
            if hasattr(self.coro, '__next__'):
                # Generator-based coroutine
                result = next(self.coro)
                if result is None:
                    return
                elif hasattr(result, '__await__'):
                    # Nested await
                    nested_task = self.loop.create_task(result)
                    nested_task.step()
                    if nested_task.done:
                        self.coro.send(nested_task.result)
            else:
                # Regular function
                self.result = self.coro
                self.done = True
        except StopIteration as e:
            self.result = e.value
            self.done = True
        except Exception as e:
            self.exception = e
            self.done = True

# Async function decorators
def async_func(func):
    def wrapper(*args, **kwargs):
        # Create a generator that yields control
        def coroutine():
            result = func(*args, **kwargs)
            return result
        return coroutine()
    return wrapper

def await_func(future):
    # In a real implementation, this would yield control to the event loop
    # For now, we'll just return the result directly
    if hasattr(future, 'result'):
        return future.result()
    return future

# Global event loop
_event_loop = EventLoop()

# ANSI Color Codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Enhanced Web Helper Functions
def http_get(url, headers=None, params=None):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8'), 'headers': dict(response.headers)}

def http_post(url, data, headers=None):
    if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers or {}, method='POST')
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8'), 'headers': dict(response.headers)}

def http_put(url, data, headers=None):
    if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers or {}, method='PUT')
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8'), 'headers': dict(response.headers)}

def http_delete(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {}, method='DELETE')
    with urllib.request.urlopen(req) as response:
        return {'status': response.status, 'text': response.read().decode('utf-8'), 'headers': dict(response.headers)}

def http_request(method, url, data=None, headers=None, params=None):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    
    if data and isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req) as response:
        return {
            'status': response.status,
            'text': response.read().decode('utf-8'),
            'headers': dict(response.headers),
            'url': url
        }

def download_file(url, filename, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())
    return {'status': 'success', 'filename': filename, 'url': url}

def get_content_type(url):
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req) as response:
        return response.headers.get('Content-Type', 'unknown')

def html_parse(html_string):
    """Simple HTML tag extraction"""
    import re
    # Extract all tags
    tags = re.findall(r'<([^>]+)>', html_string)
    # Extract text content
    text_content = re.sub(r'<[^>]+>', ' ', html_string)
    text_content = re.sub(r'\s+', ' ', text_content).strip()
    return {'tags': tags, 'text': text_content}

def html_extract_links(html_string):
    """Extract all href links from HTML"""
    import re
    links = re.findall(r'href=["\']([^"\']*)["\']', html_string)
    return links

def html_extract_images(html_string):
    """Extract all image sources from HTML"""
    import re
    images = re.findall(r'src=["\']([^"\']*)["\']', html_string)
    return images

def css_parse(css_string):
    """Simple CSS rule parsing"""
    import re
    rules = {}
    # Split by closing braces to get rule blocks
    blocks = css_string.split('}')
    for block in blocks:
        if block.strip():
            parts = block.split('{')
            if len(parts) == 2:
                selector = parts[0].strip()
                properties = parts[1].strip()
                # Parse properties
                prop_dict = {}
                prop_pairs = properties.split(';')
                for prop in prop_pairs:
                    if ':' in prop:
                        key, value = prop.split(':', 1)
                        prop_dict[key.strip()] = value.strip()
                rules[selector] = prop_dict
    return rules

def html_form_data(html_string, form_id=None):
    """Extract form data structure from HTML"""
    import re
    forms = []
    # Find all forms
    form_matches = re.findall(r'<form[^>]*>(.*?)</form>', html_string, re.DOTALL)
    for form_html in form_matches:
        form_data = {}
        # Extract action and method
        action_match = re.search(r'action=["\']([^"\']*)["\']', form_html)
        method_match = re.search(r'method=["\']([^"\']*)["\']', form_html)
        
        form_data['action'] = action_match.group(1) if action_match else ''
        form_data['method'] = method_match.group(1).upper() if method_match else 'GET'
        
        # Extract input fields
        inputs = []
        input_matches = re.findall(r'<input[^>]*>', form_html)
        for input_tag in input_matches:
            input_data = {}
            name_match = re.search(r'name=["\']([^"\']*)["\']', input_tag)
            type_match = re.search(r'type=["\']([^"\']*)["\']', input_tag)
            value_match = re.search(r'value=["\']([^"\']*)["\']', input_tag)
            
            if name_match:
                input_data['name'] = name_match.group(1)
                input_data['type'] = type_match.group(1) if type_match else 'text'
                input_data['value'] = value_match.group(1) if value_match else ''
                inputs.append(input_data)
        
        form_data['inputs'] = inputs
        forms.append(form_data)
    
    return forms[0] if form_id is None and forms else forms

def create_web_server(port=8000):
    """Create a simple web server configuration"""
    return {
        'port': port,
        'routes': {},
        'middleware': [],
        'static_files': {},
        'templates': {}
    }

def add_route(server, path, method, handler):
    """Add a route to web server"""
    route_key = method.upper() + ' ' + path
    server['routes'][route_key] = handler
    return server

def add_middleware(server, middleware_func):
    """Add middleware to web server"""
    server['middleware'].append(middleware_func)
    return server

def serve_static_file(server, url_path, file_path):
    """Add static file serving"""
    server['static_files'][url_path] = file_path
    return server

def render_template(template_string, context):
    """Simple template rendering with variable substitution"""
    result = template_string
    for key, value in context.items():
        placeholder = '{{' + key + '}}'
        result = result.replace(placeholder, str(value))
    return result

def validate_json_schema(data, schema):
    """Simple JSON schema validation"""
    errors = []
    
    for field, field_type in schema.items():
        if field not in data:
            errors.append(f'Missing required field: {field}')
        elif field_type == 'string' and not isinstance(data[field], str):
            errors.append(f'Field {field} should be string')
        elif field_type == 'number' and not isinstance(data[field], (int, float)):
            errors.append(f'Field {field} should be number')
        elif field_type == 'boolean' and not isinstance(data[field], bool):
            errors.append(f'Field {field} should be boolean')
        elif field_type == 'array' and not isinstance(data[field], list):
            errors.append(f'Field {field} should be array')
        elif field_type == 'object' and not isinstance(data[field], dict):
            errors.append(f'Field {field} should be object')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def create_api_response(status, data, message=None):
    """Create standardized API response"""
    response = {
        'status': status,
        'data': data
    }
    if message:
        response['message'] = message
    return response

def jwt_encode(payload, secret, algorithm='HS256'):
    """Simple JWT encoding (basic implementation)"""
    import hmac
    import hashlib
    import json
    import base64
    
    # Create header
    header = {'typ': 'JWT', 'alg': algorithm}
    header_json = json.dumps(header)
    header_b64 = base64.b64encode(header_json.encode()).decode()
    
    # Create payload
    payload_json = json.dumps(payload)
    payload_b64 = base64.b64encode(payload_json.encode()).decode()
    
    # Create signature
    signing_input = header_b64 + '.' + payload_b64
    signature = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()
    
    return header_b64 + '.' + payload_b64 + '.' + signature_b64

def jwt_decode(token, secret):
    """Simple JWT decoding (basic implementation)"""
    import hmac
    import hashlib
    import json
    import base64
    
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature
        signing_input = header_b64 + '.' + payload_b64
        expected_signature = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
        expected_signature_b64 = base64.b64encode(expected_signature).decode()
        
        if signature_b64 != expected_signature_b64:
            return None
        
        # Decode payload
        payload_json = base64.b64decode(payload_b64).decode()
        return json.loads(payload_json)
    except:
        return None

def base64_encode(s): return base64.b64encode(s.encode('utf-8')).decode('utf-8')
def base64_decode(s): return base64.b64decode(s).decode('utf-8')
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
def sha1(s): return hashlib.sha1(s.encode('utf-8')).hexdigest()
def sha256(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode}
def get_env(var): return os.environ.get(var)
def set_env(var, value): os.environ[var] = value
def get_cwd(): return os.getcwd()
def change_dir(path): os.chdir(path)
def list_dir(path): return os.listdir(path)
def exists(path): return os.path.exists(path)
def random_int(min_val, max_val): return random.randint(min_val, max_val)
def random_string(length): return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
def parse_url(url):
    parsed = urllib.parse.urlparse(url)
    return {'scheme': parsed.scheme, 'netloc': parsed.netloc, 'path': parsed.path, 'query': urllib.parse.parse_qs(parsed.query), 'fragment': parsed.fragment}
def url_encode(s): return urllib.parse.quote(s)
def url_decode(s): return urllib.parse.unquote(s)
def json_encode(obj): return json.dumps(obj)
def json_decode(s): return json.loads(s)
def time_now(): return time.time()
def time_sleep(seconds): time.sleep(seconds)

# Token Types
operator_pattern = r'>>>=|>>>|<<=|<<|>>=|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\+\+|--|==|!=|<=|>=|&&|\|\||//|[+\-*/%=<>!&|^~?:]'
TOKENS = [
    ('IMPORT', r'\bimport\b'), ('FROM', r'\bfrom\b'), ('CLASS', r'\bclass\b'), ('INTERFACE', r'\binterface\b'),
    ('IMPLEMENTS', r'\bimplements\b'), ('VAR', r'\bvar\b'), ('FUNC', r'\bfunc\b'), ('IF', r'\bif\b'), ('ELSE', r'\belse\b'),
    ('WHILE', r'\bwhile\b'), ('DO', r'\bdo\b'), ('FOR', r'\bfor\b'), ('IN', r'\bin\b'),
    ('BREAK', r'\bbreak\b'), ('CONTINUE', r'\bcontinue\b'), ('PRINT', r'\bprint\b'),
    ('RETURN', r'\breturn\b'), ('TRY', r'\btry\b'), ('CATCH', r'\bcatch\b'),
    ('TRUE', r'\btrue\b'), ('FALSE', r'\bfalse\b'), ('NULL', r'\bnull\b'),
    ('SET', r'\bset\b'),
    ('INSTANCEOF', r'\binstanceof\b'),
    ('NUMBER', r'\d+\.\d*|\.\d+|\d+'), ('STRING', r'"[^"]*"'), ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('OPERATOR', operator_pattern),
    ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('LBRACKET', r'\['), ('RBRACKET', r'\]'), ('COMMA', r','), ('COLON', r':'),
    ('SEMI', r';'), ('DOT', r'\.'), ('NEWLINE', r'\n'),
]

# AST Nodes
Program = namedtuple('Program', ['statements'])
ImportStmt = namedtuple('ImportStmt', ['module'])
FromImportStmt = namedtuple('FromImportStmt', ['module', 'names'])
ClassDef = namedtuple('ClassDef', ['name', 'base', 'interfaces', 'body'])
InterfaceDef = namedtuple('InterfaceDef', ['name', 'methods'])
VarDecl = namedtuple('VarDecl', ['name', 'value'])
FuncDef = namedtuple('FuncDef', ['name', 'params', 'body'])
TryStmt = namedtuple('TryStmt', ['try_block', 'catch_var', 'catch_block'])
IfStmt = namedtuple('IfStmt', ['condition', 'then_branch', 'else_branch'])
WhileStmt = namedtuple('WhileStmt', ['condition', 'body'])
DoWhileStmt = namedtuple('DoWhileStmt', ['body', 'condition'])
ForStmt = namedtuple('ForStmt', ['init', 'condition', 'increment', 'body'])
ForInStmt = namedtuple('ForInStmt', ['var', 'iterable', 'body'])
BreakStmt = namedtuple('BreakStmt', [])
ContinueStmt = namedtuple('ContinueStmt', [])
PrintStmt = namedtuple('PrintStmt', ['expression'])
ReturnStmt = namedtuple('ReturnStmt', ['expression'])
ExprStmt = namedtuple('ExprStmt', ['expression'])
AssignStmt = namedtuple('AssignStmt', ['target', 'value'])
BinaryOp = namedtuple('BinaryOp', ['left', 'op', 'right'])
UnaryOp = namedtuple('UnaryOp', ['op', 'operand'])
PrefixOp = namedtuple('PrefixOp', ['op', 'operand'])
PostfixOp = namedtuple('PostfixOp', ['operand', 'op'])
TernaryOp = namedtuple('TernaryOp', ['condition', 'true_expr', 'false_expr'])
FuncCall = namedtuple('FuncCall', ['func_expr', 'args'])
ListLiteral = namedtuple('ListLiteral', ['elements'])
DictLiteral = namedtuple('DictLiteral', ['pairs'])
SetLiteral = namedtuple('SetLiteral', ['elements'])
Identifier = namedtuple('Identifier', ['name'])
Number = namedtuple('Number', ['value'])
String = namedtuple('String', ['value'])
Boolean = namedtuple('Boolean', ['value'])
Null = namedtuple('Null', [])
IndexExpr = namedtuple('IndexExpr', ['object', 'index'])
Slice = namedtuple('Slice', ['start', 'end'])
AttributeExpr = namedtuple('AttributeExpr', ['object', 'attribute'])

# Exceptions
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.line = 1
        
    def tokenize(self):
        while self.pos < len(self.code):
            if self.code[self.pos] == '#':
                while self.pos < len(self.code) and self.code[self.pos] != '\n':
                    self.pos += 1
                continue
            match = None
            for token_type, pattern in TOKENS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    value = match.group(0)
                    if token_type == 'NEWLINE':
                        self.line += 1
                        if not self.tokens or self.tokens[-1][0] != 'NEWLINE':
                            self.tokens.append((token_type, value, self.line))
                    else:
                        self.tokens.append((token_type, value, self.line))
                    self.pos = match.end()
                    break
            if not match:
                if self.code[self.pos].isspace():
                    self.pos += 1
                else:
                    raise SyntaxError(f"Line {self.line}: Unexpected character '{self.code[self.pos]}'")
        return self.tokens

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type, value=None, optional=False):
        token = self.current_token()
        if token and token[0] == token_type and (value is None or token[1] == value):
            self.advance()
            return True
        elif optional and (token is None or token[0] == 'NEWLINE'):
            return True
        line = token[2] if token else "unknown"
        raise SyntaxError(f"Line {line}: Expected {token_type} {value or ''}, got {token}")
    
    def parse(self):
        return self.parse_program()
    
    def parse_program(self):
        statements = []
        while self.current_token():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            if self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        return Program(statements)
    
    def parse_statement(self):
        while self.current_token() and self.current_token()[0] == 'NEWLINE':
            self.advance()
        token = self.current_token()
        if not token:
            return None
        if token[0] == 'IMPORT':
            return self.parse_import_stmt()
        elif token[0] == 'FROM':
            return self.parse_from_import_stmt()
        elif token[0] == 'CLASS':
            return self.parse_class_def()
        elif token[0] == 'INTERFACE':
            return self.parse_interface_def()
        elif token[0] == 'VAR':
            return self.parse_var_decl()
        elif token[0] == 'FUNC':
            return self.parse_func_def()
        elif token[0] == 'TRY':
            return self.parse_try_stmt()
        elif token[0] == 'IF':
            return self.parse_if_stmt()
        elif token[0] == 'WHILE':
            return self.parse_while_stmt()
        elif token[0] == 'DO':
            return self.parse_do_while_stmt()
        elif token[0] == 'FOR':
            return self.parse_for_stmt()
        elif token[0] == 'BREAK':
            self.advance()
            self.expect('SEMI', optional=True)
            return BreakStmt()
        elif token[0] == 'CONTINUE':
            self.advance()
            self.expect('SEMI', optional=True)
            return ContinueStmt()
        elif token[0] == 'PRINT':
            return self.parse_print_stmt()
        elif token[0] == 'RETURN':
            return self.parse_return_stmt()
        else:
            expr = self.parse_expression()
            if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>='):
                op = self.current_token()[1]
                self.advance()
                value = self.parse_expression()
                if isinstance(expr, (Identifier, IndexExpr, AttributeExpr)):
                    if op == '=':
                        return AssignStmt(expr, value)
                    else:
                        base_op = op[:-1]
                        return AssignStmt(expr, BinaryOp(expr, base_op, value))
                raise SyntaxError("Invalid assignment target")
            self.expect('SEMI', optional=True)
            return ExprStmt(expr)
    
    def parse_import_stmt(self):
        self.advance()
        module = self.current_token()[1]
        self.advance()
        self.expect('SEMI', optional=True)
        return ImportStmt(module)
    
    def parse_from_import_stmt(self):
        self.advance()
        module = self.current_token()[1]
        self.advance()
        self.expect('IMPORT', 'import')
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '*':
            self.advance()
            names = ['*']
        else:
            names = []
            while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                names.append(self.current_token()[1])
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
        self.expect('SEMI', optional=True)
        return FromImportStmt(module, names)
    
    def parse_class_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        base = None
        interfaces = []
        if self.current_token() and self.current_token()[0] == 'LPAREN':
            self.advance()
            base = self.current_token()[1]
            self.advance()
            self.expect('RPAREN', ')')
        if self.current_token() and self.current_token()[0] == 'IMPLEMENTS':
            self.advance()
            while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                interfaces.append(self.current_token()[1])
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return ClassDef(name, base, interfaces, body)
    
    def parse_interface_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('LBRACE', '{')
        methods = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            if self.current_token()[0] == 'FUNC':
                self.advance()
                method_name = self.current_token()[1]
                self.advance()
                self.expect('LPAREN', '(')
                params = self.parse_param_list()
                self.expect('RPAREN', ')')
                self.expect('SEMI', optional=True)
                methods.append((method_name, params))
            else:
                self.advance()
        self.expect('RBRACE', '}')
        return InterfaceDef(name, methods)
    
    def parse_var_decl(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('OPERATOR', '=')
        value = self.parse_expression()
        self.expect('SEMI', optional=True)
        return VarDecl(name, value)
    
    def parse_func_def(self):
        self.advance()
        name = self.current_token()[1]
        self.advance()
        self.expect('LPAREN', '(')
        params = self.parse_param_list()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return FuncDef(name, params, body)
    
    def parse_try_stmt(self):
        self.advance()
        self.expect('LBRACE', '{')
        try_block = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                try_block.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        self.expect('CATCH', 'catch')
        self.expect('LPAREN', '(')
        catch_var = self.current_token()[1]
        self.advance()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        catch_block = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                catch_block.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return TryStmt(try_block, catch_var, catch_block)
    
    def parse_param_list(self):
        params = []
        while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
            params.append(self.current_token()[1])
            self.advance()
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        return params
    
    def parse_if_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        then_branch = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                then_branch.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        else_branch = []
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.advance()
            if self.current_token() and self.current_token()[0] == 'IF':
                else_branch = [self.parse_if_stmt()]
            else:
                self.expect('LBRACE', '{')
                while self.current_token() and self.current_token()[0] != 'RBRACE':
                    stmt = self.parse_statement()
                    if stmt:
                        else_branch.append(stmt)
                    while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                        self.advance()
                self.expect('RBRACE', '}')
        return IfStmt(condition, then_branch, else_branch)
    
    def parse_while_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        return WhileStmt(condition, body)
    
    def parse_do_while_stmt(self):
        self.advance()
        self.expect('LBRACE', '{')
        body = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                self.advance()
        self.expect('RBRACE', '}')
        self.expect('WHILE', 'while')
        self.expect('LPAREN', '(')
        condition = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('SEMI', optional=True)
        return DoWhileStmt(body, condition)
    
    def parse_for_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        if self.current_token() and self.current_token()[0] == 'IDENTIFIER' and self.tokens[self.pos + 1][0] == 'IN':
            var = self.current_token()[1]
            self.advance()
            self.expect('IN', 'in')
            iterable = self.parse_expression()
            self.expect('RPAREN', ')')
            self.expect('LBRACE', '{')
            body = []
            while self.current_token() and self.current_token()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                    self.advance()
            self.expect('RBRACE', '}')
            return ForInStmt(var, iterable, body)
        else:
            init = self.parse_var_decl() if self.current_token() and self.current_token()[0] == 'VAR' else (self.parse_expression() if self.current_token() and self.current_token()[0] != 'SEMI' else None)
            self.expect('SEMI', ';')
            condition = self.parse_expression() if self.current_token() and self.current_token()[0] != 'SEMI' else None
            self.expect('SEMI', ';')
            increment = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RPAREN' else None
            self.expect('RPAREN', ')')
            self.expect('LBRACE', '{')
            body = []
            while self.current_token() and self.current_token()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
                while self.current_token() and self.current_token()[0] in ('NEWLINE', 'SEMI'):
                    self.advance()
            self.expect('RBRACE', '}')
            return ForStmt(init, condition, increment, body)
    
    def parse_print_stmt(self):
        self.advance()
        self.expect('LPAREN', '(')
        expr = self.parse_expression()
        self.expect('RPAREN', ')')
        self.expect('SEMI', optional=True)
        return PrintStmt(expr)
    
    def parse_return_stmt(self):
        self.advance()
        if self.current_token() and (self.current_token()[0] == 'SEMI' or self.current_token()[0] == 'NEWLINE'):
            self.advance()
            return ReturnStmt(None)
        expr = self.parse_expression()
        self.expect('SEMI', optional=True)
        return ReturnStmt(expr)
    
    def parse_expression(self):
        expr = self.parse_logical_or()
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '?':
            self.advance()
            true_expr = self.parse_expression()
            self.expect('OPERATOR', ':')
            false_expr = self.parse_expression()
            expr = TernaryOp(expr, true_expr, false_expr)
        return expr
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '||':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self):
        left = self.parse_bitwise_or()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '&&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_or()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_or(self):
        left = self.parse_bitwise_xor()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '|':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_xor()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_xor(self):
        left = self.parse_bitwise_and()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '^':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_bitwise_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_bitwise_and(self):
        left = self.parse_equality()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] == '&':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self):
        left = self.parse_relational()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('==', '!='):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_relational()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_relational(self):
        left = self.parse_shift()
        while self.current_token() and ((self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('<', '>', '<=', '>=')) or self.current_token()[0] == 'INSTANCEOF'):
            if self.current_token()[0] == 'OPERATOR':
                op = self.current_token()[1]
            else:
                op = 'instanceof'
            self.advance()
            right = self.parse_shift()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_shift(self):
        left = self.parse_additive()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('<<', '>>', '>>>'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('+', '-'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('*', '/', '//', '%'):
            op = self.current_token()[1]
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_unary(self):
        if self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('-', '+', '!', '~', '++', '--'):
            op = self.current_token()[1]
            self.advance()
            operand = self.parse_unary()
            if op in ('++', '--'):
                return PrefixOp(op, operand)
            else:
                return UnaryOp(op, operand)
        return self.parse_primary()
    
    def parse_primary(self):
        token = self.current_token()
        if not token:
            raise SyntaxError("Unexpected end of input")
        if token[0] == 'IDENTIFIER':
            self.advance()
            expr = Identifier(token[1])
        elif token[0] == 'NUMBER':
            self.advance()
            num_str = token[1]
            expr = Number(float(num_str) if '.' in num_str else int(num_str))
        elif token[0] == 'STRING':
            self.advance()
            expr = String(token[1][1:-1])
        elif token[0] == 'TRUE':
            self.advance()
            expr = Boolean(True)
        elif token[0] == 'FALSE':
            self.advance()
            expr = Boolean(False)
        elif token[0] == 'NULL':
            self.advance()
            expr = Null()
        elif token[0] == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN', ')')
        elif token[0] == 'LBRACKET':
            expr = self.parse_list_literal()
        elif token[0] == 'LBRACE':
            expr = self.parse_dict_literal()
        elif token[0] == 'SET':
            self.advance()
            self.expect('LPAREN', '(')
            elements = []
            if self.current_token() and self.current_token()[0] != 'RPAREN':
                elements.append(self.parse_expression())
                while self.current_token() and self.current_token()[0] == 'COMMA':
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect('RPAREN', ')')
            expr = SetLiteral(elements)
        else:
            raise SyntaxError(f"Line {token[2]}: Unexpected token: {token}")
        
        while self.current_token() and self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('++', '--'):
            op = self.current_token()[1]
            self.advance()
            expr = PostfixOp(expr, op)
        
        while self.current_token() and self.current_token()[0] in ('DOT', 'LPAREN', 'LBRACKET'):
            if self.current_token()[0] == 'DOT':
                self.advance()
                if self.current_token() and self.current_token()[0] == 'IDENTIFIER':
                    attr = self.current_token()[1]
                    self.advance()
                    expr = AttributeExpr(expr, attr)
                else:
                    raise SyntaxError("Expected identifier after dot")
            elif self.current_token()[0] == 'LPAREN':
                self.advance()
                args = []
                while self.current_token() and self.current_token()[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.current_token() and self.current_token()[0] == 'COMMA':
                        self.advance()
                self.expect('RPAREN', ')')
                expr = FuncCall(expr, args)
            elif self.current_token()[0] == 'LBRACKET':
                self.advance()
                if self.current_token() and self.current_token()[0] == 'COLON':
                    self.advance()
                    end = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RBRACKET' else None
                    expr = IndexExpr(expr, Slice(None, end))
                else:
                    start = self.parse_expression()
                    if self.current_token() and self.current_token()[0] == 'COLON':
                        self.advance()
                        end = self.parse_expression() if self.current_token() and self.current_token()[0] != 'RBRACKET' else None
                        expr = IndexExpr(expr, Slice(start, end))
                    else:
                        expr = IndexExpr(expr, start)
                self.expect('RBRACKET', ']')
        return expr
    
    def parse_list_literal(self):
        self.advance()
        elements = []
        while self.current_token() and self.current_token()[0] != 'RBRACKET':
            elements.append(self.parse_expression())
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        self.expect('RBRACKET', ']')
        return ListLiteral(elements)
    
    def parse_dict_literal(self):
        self.advance()
        pairs = []
        while self.current_token() and self.current_token()[0] != 'RBRACE':
            key = self.parse_expression()
            self.expect('COLON', ':')
            value = self.parse_expression()
            pairs.append((key, value))
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.advance()
        self.expect('RBRACE', '}')
        return DictLiteral(pairs)

# Class Object
class ShiboClass:
    def __init__(self, name, base, interfaces, env, methods, attributes):
        self.name = name
        self.base = base
        self.interfaces = interfaces
        self.env = env
        self.methods = methods
        self.attributes = attributes
    
    def instantiate(self, interpreter, args):
        instance = ShiboInstance(self, interpreter)
        if 'init' in self.methods:
            method = self.methods['init']
            if len(args) != len(method.params) - 1:  # -1 for 'self'
                raise TypeError(f"Expected {len(method.params) - 1} arguments, got {len(args)}")
            local_env = {'self': instance}
            local_env.update({param: arg for param, arg in zip(method.params[1:], args)})
            try:
                interpreter.eval(Program(method.body), local_env)
            except ReturnException:
                pass  # init doesn't return anything
        return instance

class ShiboInstance:
    def __init__(self, cls, interpreter):
        self.cls = cls
        self.env = {}
        self.env.update(cls.attributes)
        if cls.base:
            base_cls = interpreter.env.get(cls.base)
            if base_cls and isinstance(base_cls, ShiboClass):
                self.env.update(base_cls.attributes)

# Interpreter
class Interpreter:
    def __init__(self):
        self.env = {
            'append': lambda lst, val: lst.append(val) or lst,
            'remove': lambda lst, val: lst.remove(val) or lst,
            'pop': lambda lst, idx=None: lst.pop(idx if idx is not None else -1),
            'sort': lambda lst: lst.sort() or lst,
            'reverse': lambda lst: lst.reverse() or lst,
            'keys': lambda d: list(d.keys()),
            'len': len,
            'range': lambda start, stop: list(range(start, stop)),
            'input': input,
            'type': lambda x: type(x).__name__,
            'str': str,
            'int': int,
            'float': float,
            'upper': lambda s: s.upper(),
            'lower': lambda s: s.lower(),
            'split': lambda s, sep=None: s.split(sep),
            'math': {'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'pi': math.pi, 'pow': math.pow, 'exp': math.exp},
            'image': {'load': lambda path: Image.open(path), 'show': lambda img: img.show() or None},
            'file': {'read': lambda path: open(path, 'r').read(), 'write': lambda path, content: open(path, 'w').write(content) or None},
            'net': {
                'http_get': http_get, 
                'http_post': http_post,
                'http_put': http_put,
                'http_delete': http_delete,
                'http_request': http_request,
                'download_file': download_file,
                'get_content_type': get_content_type
            },
            'crypto': {'md5': md5, 'sha1': sha1, 'sha256': sha256},
            'os': {'get_env': get_env, 'set_env': set_env, 'get_cwd': get_cwd, 'change_dir': change_dir, 'list_dir': list_dir, 'exists': exists, 'run_command': run_command},
            'random': {'int': random_int, 'string': random_string},
            'url': {'parse': parse_url, 'encode': url_encode, 'decode': url_decode},
            'base64': {'encode': base64_encode, 'decode': base64_decode},
            # Advanced data structures
            'Set': Set,
            'Queue': Queue,
            'Stack': Stack,
            'PriorityQueue': PriorityQueue,
            # Functional programming utilities
            'map': map_func,
            'filter': filter_func,
            'reduce': reduce_func,
            'compose': compose,
            'partial': partial,
            # Advanced algorithms
            'sort_list': lambda lst, reverse=False: sorted(lst, reverse=reverse),
            'binary_search': lambda lst, target: _binary_search(lst, target, 0, len(lst) - 1),
            'quick_sort': lambda lst: _quick_sort(lst[:]),
            'merge_sort': lambda lst: _merge_sort(lst[:]),
            # Advanced utilities
            'deep_copy': lambda obj: _deep_copy(obj),
            'flatten_list': lambda lst: _flatten_list(lst),
            'chunk_list': lambda lst, size: [lst[i:i + size] for i in range(0, len(lst), size)],
            'unique_list': lambda lst: list(dict.fromkeys(lst)),
            'group_by': lambda lst, key_func: _group_by(lst, key_func),
            'debounce': lambda func, delay: _debounce(func, delay),
            'memoize': lambda func: _memoize(func),
            # Async/Await support
            'async': async_func,
            'await': await_func,
            'create_task': lambda coro: _event_loop.create_task(coro),
            'run_async': lambda: _event_loop.run_until_complete(),
            'sleep_async': lambda seconds: _event_loop.run_in_thread(time.sleep, seconds),
            # Enhanced error handling
            'ShiboException': ShiboException,
            'ValidationError': ValidationError,
            'NetworkError': NetworkError,
            'DatabaseError': DatabaseError,
            'FileNotFoundError': FileNotFoundError,
            'PermissionError': PermissionError,
            'try_catch': try_catch,
            'assert': assert_condition,
            'validate_type': validate_type,
            'validate_range': validate_range,
            # Database ORM
            'Database': Database,
            'Model': Model,
            'QueryBuilder': QueryBuilder,
            'create_database': create_database,
            'create_model': create_model,
            'query_builder': query_builder,
            # Module System
            'Module': Module,
            'ModuleLoader': ModuleLoader,
            'import': import_module,
            'export': export_to_module,
            'create_module': create_module,
            # Logging and Monitoring
            'Logger': Logger,
            'MetricsCollector': MetricsCollector,
            'HealthChecker': HealthChecker,
            'create_logger': create_logger,
            'log_debug': log_debug,
            'log_info': log_info,
            'log_warn': log_warn,
            'log_error': log_error,
            'log_fatal': log_fatal,
            'get_logs': get_logs,
            'metric_increment': metric_increment,
            'metric_set': metric_set,
            'metric_get': metric_get,
            'start_timer': start_timer,
            'stop_timer': stop_timer,
            'get_metrics': get_metrics,
            'reset_metrics': reset_metrics,
            'add_health_check': add_health_check,
            'run_health_check': run_health_check,
            'run_all_health_checks': run_all_health_checks,
            'get_health_status': get_health_status,
            're': {'search': lambda pattern, string: re.search(pattern, string).groups() if re.search(pattern, string) else None,
                   'match': lambda pattern, string: re.match(pattern, string).groups() if re.match(pattern, string) else None,
                   'findall': lambda pattern, string: re.findall(pattern, string)},
            'json': {'encode': json_encode, 'decode': json_decode},
            'time': {'now': time_now, 'sleep': time_sleep},
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'set_union': lambda s1, s2: s1.union(s2),
            'set_intersection': lambda s1, s2: s1.intersection(s2),
            'set_difference': lambda s1, s2: s1.difference(s2),
            'set_symmetric_difference': lambda s1, s2: s1.symmetric_difference(s2),
            'set_add': lambda s, elem: s.add(elem) or s,
            'set_remove': lambda s, elem: s.remove(elem) or s,
            'datetime': {
                'now': datetime.datetime.now,
                'strftime': lambda dt, fmt: dt.strftime(fmt),
                'strptime': lambda s, fmt: datetime.datetime.strptime(s, fmt),
                'date': datetime.date,
                'time': datetime.time,
                'timedelta': datetime.timedelta,
            },
            'web': {
                'html_parse': html_parse,
                'html_extract_links': html_extract_links,
                'html_extract_images': html_extract_images,
                'css_parse': css_parse,
                'html_form_data': html_form_data,
                'create_web_server': create_web_server,
                'add_route': add_route,
                'add_middleware': add_middleware,
                'serve_static_file': serve_static_file,
                'render_template': render_template,
                'validate_json_schema': validate_json_schema,
                'create_api_response': create_api_response,
                'jwt_encode': jwt_encode,
                'jwt_decode': jwt_decode
            },
        }
        self.loop_depth = 0
        self.modules = {}
    
    def eval(self, node, env=None):
        env = env if env is not None else self.env
        if isinstance(node, Program):
            return self.eval_program(node, env)
        elif isinstance(node, ImportStmt):
            return self.eval_import_stmt(node, env)
        elif isinstance(node, FromImportStmt):
            return self.eval_from_import_stmt(node, env)
        elif isinstance(node, ClassDef):
            return self.eval_class_def(node, env)
        elif isinstance(node, InterfaceDef):
            return self.eval_interface_def(node, env)
        elif isinstance(node, VarDecl):
            return self.eval_var_decl(node, env)
        elif isinstance(node, FuncDef):
            return self.eval_func_def(node, env)
        elif isinstance(node, TryStmt):
            return self.eval_try_stmt(node, env)
        elif isinstance(node, AssignStmt):
            return self.eval_assign_stmt(node, env)
        elif isinstance(node, IfStmt):
            return self.eval_if_stmt(node, env)
        elif isinstance(node, WhileStmt):
            return self.eval_while_stmt(node, env)
        elif isinstance(node, DoWhileStmt):
            return self.eval_do_while_stmt(node, env)
        elif isinstance(node, ForStmt):
            return self.eval_for_stmt(node, env)
        elif isinstance(node, ForInStmt):
            return self.eval_for_in_stmt(node, env)
        elif isinstance(node, BreakStmt):
            return self.eval_break_stmt()
        elif isinstance(node, ContinueStmt):
            return self.eval_continue_stmt()
        elif isinstance(node, PrintStmt):
            return self.eval_print_stmt(node, env)
        elif isinstance(node, ReturnStmt):
            return self.eval_return_stmt(node, env)
        elif isinstance(node, ExprStmt):
            return self.eval_expr_stmt(node, env)
        elif isinstance(node, Identifier):
            return env.get(node.name, self.env.get(node.name))
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
        elif isinstance(node, Null):
            return None
        elif isinstance(node, ListLiteral):
            return [self.eval(e, env) for e in node.elements]
        elif isinstance(node, DictLiteral):
            return {self.eval(k, env): self.eval(v, env) for k, v in node.pairs}
        elif isinstance(node, SetLiteral):
            return set(self.eval(e, env) for e in node.elements)
        elif isinstance(node, BinaryOp):
            return self.eval_binary_op(node, env)
        elif isinstance(node, UnaryOp):
            return self.eval_unary_op(node, env)
        elif isinstance(node, PrefixOp):
            return self.eval_prefix_op(node, env)
        elif isinstance(node, PostfixOp):
            return self.eval_postfix_op(node, env)
        elif isinstance(node, TernaryOp):
            return self.eval_ternary_op(node, env)
        elif isinstance(node, FuncCall):
            return self.eval_func_call(node, env)
        elif isinstance(node, IndexExpr):
            return self.eval_index_expr(node, env)
        elif isinstance(node, AttributeExpr):
            return self.eval_attribute_expr(node, env)
    
    def get_lvalue(self, node, env):
        if isinstance(node, Identifier):
            return env[node.name]
        elif isinstance(node, IndexExpr):
            obj = self.eval(node.object, env)
            index = self.eval(node.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                return obj[index]
            else:
                raise TypeError("Cannot index non-list or non-dict")
        elif isinstance(node, AttributeExpr):
            obj = self.eval(node.object, env)
            if isinstance(obj, ShiboInstance):
                return obj.env[node.attribute]
            elif isinstance(obj, dict):
                return obj[node.attribute]
            else:
                try:
                    return getattr(obj, node.attribute)
                except AttributeError:
                    raise AttributeError(f"'{type(obj).__name__}' has no attribute '{node.attribute}'")
        else:
            raise TypeError("Invalid lvalue")
    
    def set_lvalue(self, node, value, env):
        if isinstance(node, Identifier):
            env[node.name] = value
        elif isinstance(node, IndexExpr):
            obj = self.eval(node.object, env)
            index = self.eval(node.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                obj[index] = value
            else:
                raise TypeError("Cannot assign to non-list or non-dict")
        elif isinstance(node, AttributeExpr):
            obj = self.eval(node.object, env)
            if isinstance(obj, ShiboInstance):
                obj.env[node.attribute] = value
            elif isinstance(obj, dict):
                obj[node.attribute] = value
            else:
                try:
                    setattr(obj, node.attribute, value)
                except AttributeError:
                    raise TypeError(f"Cannot set attribute '{node.attribute}' on {type(obj).__name__}")
        else:
            raise TypeError("Invalid lvalue")
    
    def eval_program(self, node, env):
        result = None
        for stmt in node.statements:
            result = self.eval(stmt, env)
        return result
    
    def eval_import_stmt(self, node, env):
        if node.module not in self.modules:
            try:
                with open(f"{node.module}.shibo", 'r') as f:
                    code = f.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                module_env = {}
                self.eval(ast, module_env)
                self.modules[node.module] = module_env
            except FileNotFoundError:
                raise ImportError(f"Module '{node.module}' not found")
        env.update(self.modules[node.module])
        return None
    
    def eval_from_import_stmt(self, node, env):
        if node.module not in self.modules:
            try:
                with open(f"{node.module}.shibo", 'r') as f:
                    code = f.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                module_env = {}
                self.eval(ast, module_env)
                self.modules[node.module] = module_env
            except FileNotFoundError:
                raise ImportError(f"Module '{node.module}' not found")
        if node.names == ['*']:
            env.update(self.modules[node.module])
        else:
            for name in node.names:
                if name in self.modules[node.module]:
                    env[name] = self.modules[node.module][name]
                else:
                    raise ImportError(f"'{name}' not found in module '{node.module}'")
        return None
    
    def eval_class_def(self, node, env):
        methods = {}
        attributes = {}
        for stmt in node.body:
            if isinstance(stmt, FuncDef):
                methods[stmt.name] = stmt
            elif isinstance(stmt, VarDecl):
                attributes[stmt.name] = self.eval(stmt.value, env)
        cls = ShiboClass(node.name, node.base, node.interfaces, env, methods, attributes)
        env[node.name] = cls
        return None
    
    def eval_interface_def(self, node, env):
        env[node.name] = {'type': 'interface', 'methods': {name: params for name, params in node.methods}}
        return None
    
    def eval_var_decl(self, node, env):
        value = self.eval(node.value, env)
        env[node.name] = value
        return None
    
    def eval_func_def(self, node, env):
        env[node.name] = node
        return None
    
    def eval_try_stmt(self, node, env):
        try:
            return self.eval_program(Program(node.try_block), env)
        except Exception as e:
            env[node.catch_var] = str(e)
            return self.eval_program(Program(node.catch_block), env)
    
    def eval_assign_stmt(self, node, env):
        value = self.eval(node.value, env)
        if isinstance(node.target, Identifier):
            env[node.target.name] = value
        elif isinstance(node.target, IndexExpr):
            obj = self.eval(node.target.object, env)
            index = self.eval(node.target.index, env)
            if isinstance(obj, list) or isinstance(obj, dict):
                obj[index] = value
            else:
                raise TypeError("Cannot assign to non-list or non-dict")
        elif isinstance(node.target, AttributeExpr):
            obj = self.eval(node.target.object, env)
            if isinstance(obj, ShiboInstance):
                obj.env[node.target.attribute] = value
            elif isinstance(obj, dict):
                obj[node.target.attribute] = value
            else:
                try:
                    setattr(obj, node.target.attribute, value)
                except AttributeError:
                    raise TypeError(f"Cannot set attribute '{node.target.attribute}' on {type(obj).__name__}")
        return None
    
    def eval_if_stmt(self, node, env):
        condition = self.eval(node.condition, env)
        if condition:
            return self.eval_program(Program(node.then_branch), env)
        elif node.else_branch:
            return self.eval_program(Program(node.else_branch), env)
        return None
    
    def eval_while_stmt(self, node, env):
        self.loop_depth += 1
        while self.eval(node.condition, env):
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
        self.loop_depth -= 1
        return None
    
    def eval_do_while_stmt(self, node, env):
        self.loop_depth += 1
        while True:
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
            if not self.eval(node.condition, env):
                break
        self.loop_depth -= 1
        return None
    
    def eval_for_stmt(self, node, env):
        self.loop_depth += 1
        if node.init:
            self.eval(node.init, env)
        while node.condition is None or self.eval(node.condition, env):
            try:
                self.eval_program(Program(node.body), env)
            except ContinueException:
                pass
            except BreakException:
                break
            if node.increment:
                self.eval(node.increment, env)
        self.loop_depth -= 1
        return None
    
    def eval_for_in_stmt(self, node, env):
        self.loop_depth += 1
        iterable = self.eval(node.iterable, env)
        for item in iterable:
            try:
                env[node.var] = item
                self.eval_program(Program(node.body), env)
            except ContinueException:
                continue
            except BreakException:
                break
        self.loop_depth -= 1
        return None
    
    def eval_break_stmt(self):
        if self.loop_depth == 0:
            raise SyntaxError("break outside loop")
        raise BreakException()
    
    def eval_continue_stmt(self):
        if self.loop_depth == 0:
            raise SyntaxError("continue outside loop")
        raise ContinueException()
    
    def eval_print_stmt(self, node, env):
        value = self.eval(node.expression, env)
        print(value)
        return None
    
    def eval_return_stmt(self, node, env):
        value = self.eval(node.expression, env) if node.expression else None
        raise ReturnException(value)
    
    def eval_expr_stmt(self, node, env):
        return self.eval(node.expression, env)
    
    def eval_prefix_op(self, node, env):
        operand = node.operand
        if not isinstance(operand, (Identifier, IndexExpr, AttributeExpr)):
            raise TypeError("Invalid operand for prefix operator")
        old_value = self.get_lvalue(operand, env)
        if not isinstance(old_value, (int, float)):
            raise TypeError("Can only increment/decrement numbers")
        if node.op == '++':
            new_value = old_value + 1
        elif node.op == '--':
            new_value = old_value - 1
        else:
            raise ValueError("Invalid prefix operator")
        self.set_lvalue(operand, new_value, env)
        return new_value
    
    def eval_postfix_op(self, node, env):
        operand = node.operand
        if not isinstance(operand, (Identifier, IndexExpr, AttributeExpr)):
            raise TypeError("Invalid operand for postfix operator")
        old_value = self.get_lvalue(operand, env)
        if not isinstance(old_value, (int, float)):
            raise TypeError("Can only increment/decrement numbers")
        if node.op == '++':
            new_value = old_value + 1
        elif node.op == '--':
            new_value = old_value - 1
        else:
            raise ValueError("Invalid postfix operator")
        self.set_lvalue(operand, new_value, env)
        return old_value
    
    def eval_ternary_op(self, node, env):
        condition = self.eval(node.condition, env)
        if condition:
            return self.eval(node.true_expr, env)
        else:
            return self.eval(node.false_expr, env)
    
    def eval_binary_op(self, node, env):
        left = self.eval(node.left, env)
        if node.op == '&&':
            return left and self.eval(node.right, env)
        elif node.op == '||':
            return left or self.eval(node.right, env)
        right = self.eval(node.right, env)
        if node.op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '//':
            return left // right
        elif node.op == '%':
            return left % right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op in ('&', '|', '^', '<<', '>>', '>>>'):
            if not isinstance(left, int) or not isinstance(right, int):
                raise TypeError("Bitwise operations require integers")
            if node.op == '&':
                return left & right
            elif node.op == '|':
                return left | right
            elif node.op == '^':
                return left ^ right
            elif node.op == '<<':
                return left << right
            elif node.op == '>>':
                return left >> right
            elif node.op == '>>>':
                return (left & 0xFFFFFFFF) >> right
        elif node.op == 'instanceof':
            if not isinstance(left, ShiboInstance):
                return False
            right_val = self.eval(node.right, env)
            if not isinstance(right_val, ShiboClass):
                return False
            cls = left.cls
            while cls:
                if cls == right_val:
                    return True
                cls = self.env.get(cls.base) if cls.base else None
            return False
    
    def eval_unary_op(self, node, env):
        operand = self.eval(node.operand, env)
        if node.op == '-':
            return -operand
        elif node.op == '+':
            return operand
        elif node.op == '!':
            return not operand
        elif node.op == '~':
            if not isinstance(operand, int):
                raise TypeError("Bitwise complement requires integer")
            return ~operand
    
    def eval_func_call(self, node, env, instance_env=None):
        func = self.eval(node.func_expr, env)
        args = [self.eval(arg, env) for arg in node.args]
        if isinstance(func, tuple) and len(func) == 2 and isinstance(func[0], FuncDef) and isinstance(func[1], ShiboInstance):
            method, instance = func
            if len(args) != len(method.params) - 1:  # -1 for 'self'
                raise TypeError(f"Expected {len(method.params) - 1} arguments, got {len(args)}")
            local_env = {'self': instance}
            local_env.update({param: arg for param, arg in zip(method.params[1:], args)})
            interpreter = Interpreter()
            interpreter.env.update(self.env)
            interpreter.env.update(local_env)
            try:
                interpreter.eval(Program(method.body))
            except ReturnException as e:
                return e.value
            return None
        elif isinstance(func, FuncDef):
            if len(args) != len(func.params):
                raise TypeError(f"Expected {len(func.params)} arguments, got {len(args)}")
            local_env = {param: arg for param, arg in zip(func.params, args)}
            interpreter = Interpreter()
            interpreter.env.update(self.env)
            if instance_env:
                local_env.update(instance_env)
            interpreter.env.update(local_env)
            try:
                interpreter.eval(Program(func.body))
            except ReturnException as e:
                return e.value
            return None
        elif isinstance(func, ShiboClass):
            return func.instantiate(self, args)
        elif callable(func):
            return func(*args)
        raise TypeError(f"'{type(func).__name__}' is not callable")
    
    def eval_index_expr(self, node, env):
        obj = self.eval(node.object, env)
        index = self.eval(node.index, env)
        if isinstance(index, Slice):
            start = self.eval(index.start, env) if index.start is not None else 0
            end = self.eval(index.end, env) if index.end is not None else len(obj)
            if isinstance(obj, list):
                return obj[start:end]
            raise TypeError("Slicing only supported on lists")
        elif isinstance(obj, list):
            return obj[index]
        elif isinstance(obj, dict):
            return obj.get(index, None)
        raise TypeError("Cannot index non-list or non-dict")
    
    def eval_attribute_expr(self, node, env):
        obj = self.eval(node.object, env)
        if isinstance(obj, ShiboInstance):
            if node.attribute in obj.env:
                return obj.env[node.attribute]
            elif node.attribute in obj.cls.methods:
                return (obj.cls.methods[node.attribute], obj)
            else:
                base_cls = obj.cls.base
                while base_cls:
                    base_cls_obj = self.env.get(base_cls)
                    if base_cls_obj and isinstance(base_cls_obj, ShiboClass):
                        if node.attribute in base_cls_obj.methods:
                            return (base_cls_obj.methods[node.attribute], obj)
                        base_cls = base_cls_obj.base
                    else:
                        break
                raise AttributeError(f"'{obj.cls.name}' instance has no attribute '{node.attribute}'")
        elif isinstance(obj, ShiboClass):
            if node.attribute in obj.methods:
                return obj.methods[node.attribute]
            else:
                raise AttributeError(f"Class '{obj.name}' has no method '{node.attribute}'")
        elif isinstance(obj, dict):
            if node.attribute in obj:
                return obj[node.attribute]
            try:
                return getattr(obj, node.attribute)
            except AttributeError:
                raise AttributeError(f"Dictionary has no key or attribute '{node.attribute}'")
        try:
            return getattr(obj, node.attribute)
        except AttributeError:
            raise AttributeError(f"'{type(obj).__name__}' has no attribute '{node.attribute}'")

# Enhanced REPL
def repl():
    interpreter = Interpreter()
    __version__ = "0.3.0"
    ICON = "🐕"
    print(f"{Colors.OKCYAN}{ICON} Welcome to ShiboScript v{__version__} REPL! Type 'exit' to quit, 'help' for help.{Colors.ENDC}")

    while True:
        try:
            code = input(f"{Colors.OKGREEN}shiboscript>>> {Colors.ENDC}")
            if code.strip() == "exit":
                break
            if code.strip() in ('cls', 'clear'):
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            if code.strip() == "help":
                print("Available built-ins:")
                for key in sorted(interpreter.env.keys()):
                    if not key.startswith('_'):
                        print(f" - {key}")
                continue
            while True:
                try:
                    lexer = Lexer(code)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    ast = parser.parse()
                    break
                except SyntaxError as e:
                    print(f"{Colors.FAIL}Syntax Error: {e}{Colors.ENDC}")
                    next_line = input(f"{Colors.WARNING}... {Colors.ENDC}")
                    if next_line.strip() == "":
                        raise
                    code += "\n" + next_line
            result = interpreter.eval(ast)
            if result is not None:
                print(f"{Colors.OKBLUE}{result}{Colors.ENDC}")
        except SyntaxError as e:
            print(f"{Colors.FAIL}Syntax Error: {e}{Colors.ENDC}")
        except NameError as e:
            print(f"{Colors.FAIL}Name Error: {e}{Colors.ENDC}")
        except TypeError as e:
            print(f"{Colors.FAIL}Type Error: {e}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

# Run Script from File
def run_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.eval(ast)
    except FileNotFoundError:
        print(f"{Colors.FAIL}File not found: {filename}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()