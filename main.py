import json

def isValid(stale, latest, otjson):
  try:
      operations = json.loads(otjson)
  except json.JSONDecodeError:
      return False

  cursor = 0
  document = list(stale)

  for op in operations:
      if op['op'] == 'skip':
          cursor += op['count']
          if cursor > len(document):
              return False
      elif op['op'] == 'insert':
          for char in op['chars']:
              document.insert(cursor, char)
              cursor += 1
      elif op['op'] == 'delete':
          if cursor + op['count'] > len(document):
              return False
          del document[cursor:cursor + op['count']]

  return ''.join(document) == latest

# Test cases
test_cases = [
  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'Repl.it uses operational transformations.',
   '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}]'),

  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'Repl.it uses operational transformations.',
   '[{"op": "skip", "count": 45}, {"op": "delete", "count": 47}]'),

  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'Repl.it uses operational transformations.',
   '[{"op": "skip", "count": 40}, {"op": "delete", "count": 47}, {"op": "skip", "count": 2}]'),

  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'We use operational transformations to keep everyone in a multiplayer repl in sync.',
   '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, {"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'),

  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'We can use operational transformations to keep everyone in a multiplayer repl in sync.',
   '[{"op": "delete", "count": 7}, {"op": "insert", "chars": "We"}, {"op": "skip", "count": 4}, {"op": "delete", "count": 1}]'),

  ('Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   'Repl.it uses operational transformations to keep everyone in a multiplayer repl in sync.',
   '[]')
]

test_results = [isValid(*test) for test in test_cases]
print(test_results)
