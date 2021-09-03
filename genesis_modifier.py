import json
from pyband.wallet import PublicKey, Address
import base64
from config import old_valop_map

with open('mock_genesis.json', 'r') as f:
    genesis = json.load(f)

print (len(genesis["app_state"]["staking"]["validators"]))
print (len(genesis["validators"]))

genesis["genesis_time"] = "2021-08-05T03:30:00Z"
genesis["chain_id"] += "-mock"

idx = 0
for i, val in enumerate(genesis["app_state"]["staking"]["validators"]):
    if val["status"] != 2:
        continue

    valop_addr = val["operator_address"]
    cons_pubkey = val["consensus_pubkey"]
    if valop_addr in old_valop_map:
        val["operator_address"] = old_valop_map[valop_addr]["new_valop"]
        val["consensus_pubkey"] = old_valop_map[valop_addr]["new_cons_pubkey"]
        assert genesis["validators"][idx]["pub_key"]["value"] == base64.b64encode(bytes.fromhex(PublicKey.from_cons_bech32(cons_pubkey).to_hex())).decode()
        genesis["validators"][idx]["pub_key"]["value"] = base64.b64encode(bytes.fromhex(PublicKey.from_cons_bech32(old_valop_map[valop_addr]["new_cons_pubkey"]).to_hex())).decode()

        cons_addr = PublicKey.from_cons_bech32(cons_pubkey).to_address().to_cons_bech32()
        new_cons_addr = PublicKey.from_cons_bech32(old_valop_map[valop_addr]["new_cons_pubkey"]).to_address().to_cons_bech32()

        if genesis["app_state"]["distribution"]["previous_proposer"] == cons_addr:
            genesis["app_state"]["distribution"]["previous_proposer"] = new_cons_addr

        genesis["app_state"]["slashing"]["missed_blocks"][new_cons_addr] = genesis["app_state"]["slashing"]["missed_blocks"][cons_addr]
        genesis["app_state"]["slashing"]["missed_blocks"].pop(cons_addr, None)

        genesis["app_state"]["slashing"]["signing_infos"][new_cons_addr] = genesis["app_state"]["slashing"]["signing_infos"][cons_addr]
        genesis["app_state"]["slashing"]["signing_infos"][new_cons_addr]["address"] = new_cons_addr
        genesis["app_state"]["slashing"]["signing_infos"].pop(cons_addr, None)
    idx += 1


addr2acc = {}
for i, acc in enumerate(genesis["app_state"]["auth"]["accounts"]):
    addr2acc[acc["value"]["address"]] = acc

for val in genesis["app_state"]["distribution"]["delegator_starting_infos"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        old_addr = Address.from_val_bech32(valop_addr).to_acc_bech32()
        if val["delegator_address"] == old_addr:
            val["delegator_address"] = old_valop_map[valop_addr]["new_addr"]
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

            
for valop_addr in old_valop_map.keys():
    old_addr = Address.from_val_bech32(valop_addr).to_acc_bech32()
    
    acc = addr2acc[old_addr]
    acc["value"]["address"] = old_valop_map[valop_addr]["new_addr"]
    acc["value"]["public_key"] = None

    for withdraw_info in genesis["app_state"]["distribution"]["delegator_withdraw_infos"]:
        if withdraw_info["delegator_address"] == old_addr:
            withdraw_info["delegator_address"] = old_valop_map[valop_addr]["new_addr"]
        if withdraw_info["withdraw_address"] == old_addr:
            withdraw_info["withdraw_address"] = old_valop_map[valop_addr]["new_addr"]
    
    for delegation in genesis["app_state"]["staking"]["delegations"]:
        if delegation["delegator_address"] == old_addr:
            delegation["delegator_address"] = old_valop_map[valop_addr]["new_addr"]
        if delegation["validator_address"] == valop_addr:
            delegation["validator_address"] = old_valop_map[valop_addr]["new_valop"]

    for redelegation in genesis["app_state"]["staking"]["redelegations"]:
        if redelegation["delegator_address"] == old_addr:
            redelegation["delegator_address"] = old_valop_map[valop_addr]["new_addr"]
        if redelegation["validator_dst_address"] == valop_addr:
            redelegation["validator_dst_address"] = old_valop_map[valop_addr]["new_valop"]
        if redelegation["validator_src_address"] == valop_addr:
            redelegation["validator_src_address"] = old_valop_map[valop_addr]["new_valop"]
    
    for unbonding_delegation in genesis["app_state"]["staking"]["unbonding_delegations"]:
        if unbonding_delegation["delegator_address"] == old_addr:
            unbonding_delegation["delegator_address"] = old_valop_map[valop_addr]["new_addr"]
        if unbonding_delegation["validator_address"] == valop_addr:
            unbonding_delegation["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["distribution"]["outstanding_rewards"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["distribution"]["validator_accumulated_commissions"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["distribution"]["validator_current_rewards"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["distribution"]["validator_historical_rewards"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["distribution"]["validator_slash_events"]:
    valop_addr = val["validator_address"]
    if valop_addr in old_valop_map:
        val["validator_address"] = old_valop_map[valop_addr]["new_valop"]

for val in genesis["app_state"]["staking"]["last_validator_powers"]:
    valop_addr = val["Address"]
    if valop_addr in old_valop_map:
        val["Address"] = old_valop_map[valop_addr]["new_valop"]

for reporter in genesis["app_state"]["oracle"]["reporters"]:
    valop_addr = reporter["validator"]
    if valop_addr in old_valop_map:
        old_addr = Address.from_val_bech32(valop_addr).to_acc_bech32()
        reporter["validator"] = old_valop_map[valop_addr]["new_valop"]
        for i in range(len(reporter["reporters"])):
            if reporter["reporters"][i] == old_addr:
                reporter["reporters"][i] = reporter["reporters"][0]
                reporter["reporters"][0] = old_valop_map[valop_addr]["new_addr"]
                break
        for i in range(5):
            acc = addr2acc[reporter["reporters"][i+1]]
            acc["value"]["address"] = old_valop_map[valop_addr]["reporters"][i]
            acc["value"]["public_key"] = None

            reporter["reporters"][i+1] = old_valop_map[valop_addr]["reporters"][i]

with open('new_genesis.json', 'w') as f:
    json.dump(genesis, f)
