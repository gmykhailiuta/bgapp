#!/bin/sh
role=green
while true; do
  if [ $role = "green" ]; then
    role="blue"
  else
    role="green"
  fi
  echo "Switching to $role.."
  ./scripts/switch.sh $role
  sleep 0.5
done
