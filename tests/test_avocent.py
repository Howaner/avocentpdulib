import json
from avocentpdulib import AvocentPdu, OutletAction
import asyncio

async def main():
	pdu = AvocentPdu("http://192.168.150.100", "admin", "avocent")

	login_response = await pdu.login()
	if not login_response.successful:
		print("Login failed.")
		exit(1)

	print("Login successful. Token: {}".format(login_response.sid))

	print("===============")
	print("Read System Info")

	system_info = await pdu.get_system_info()
	print(json.dumps(system_info.__dict__))

	print("===============")
	print("Read PDUs")

	pdus_response = await pdu.list_pdus()
	print("Found {} pdus".format(len(pdus_response.pdus)))
	for pdu1 in pdus_response.pdus:
		print("  {} ({})".format(pdu1.name, pdu1.model))
		for port in pdu1.ports:
			print("    Port {}: Id = {}, Status = {}".format(port.name, port.portid, port.status.name))

	first_pdu = pdus_response.pdus[0].name

	print("===============")
	print("Read Outlets from {}".format(first_pdu))

	outlets_response = await pdu.get_pdu_outlets(first_pdu)
	print("Found {0} outlets".format(len(outlets_response.outlets)))
	for outlet in outlets_response.outlets:
		print("  Outlet {}: Name = {}, Status = {}, Current = {}, Power = {}".format(outlet.number, outlet.name, outlet.status.name, outlet.current, outlet.power))

	print("===============")
	print("Read Outlets from {}".format(first_pdu))

	overview_response = await pdu.get_pdu_overview(first_pdu)
	print("Found {} overview entries.".format(len(overview_response.entries)))
	for entry in overview_response.entries:
		print("  {} | {}: Current = {}, Voltage = {}, Power = {}, Power Factor = {}, kWh = {}".format(entry.scope.name, entry.name, entry.current, entry.voltage, entry.power, entry.power_factor, entry.total_kwh))

	total_power_response = await pdu.get_pdu_total_powers(first_pdu)
	print("Found {} total power entries.".format(len(total_power_response.entries)))
	for entry in total_power_response.entries:
		print("  {} | {}: Start Time = {}, kWh = {}".format(entry.scope.name, entry.name, entry.start_time, entry.total_kwh))

	print("===============")
	first_outlet = outlets_response.outlets[0]
	print("Turn off and on outlet {}.{}".format(first_pdu, first_outlet.number))

	await pdu.send_outlet_action(first_pdu, first_outlet.number, OutletAction.TURN_OFF)
	await pdu.send_outlet_action(first_pdu, first_outlet.number, OutletAction.TURN_ON)

	await pdu.close()

asyncio.run(main())
