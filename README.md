# migration-test

This works with Band GuanYu network (Cosmos SDK v0.39)

1. Edit the list of validators in `config.py`
2. Back up the necessary files in `backup/`
    - `node_key.json`
    - `priv_validator.json`
    - `privkey.txt`
    - `.yoda`
3. Run `genesis_modifier.py`