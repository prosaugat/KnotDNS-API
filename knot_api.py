from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/dns/config/<domain>", methods=["POST"])
def create_config(domain):
    subprocess.run(["knotc", "conf-begin"])
    subprocess.run(["knotc", "conf-set", f"zone[{domain}]"])
    subprocess.run(["knotc", "conf-set", f"zone[{domain}].file", f"{domain}.zone"])
    subprocess.run(["knotc", "conf-commit"])
    subprocess.run(["knotc", "zone-begin", f"{domain}"])
    subprocess.run(["knotc", "zone-set", f"{domain}.", "@", "86400", "SOA", "one.dns.id.", "hostmaster.dns.id.", "2020011301", "3600", "3600", "604800", "38400"])
    subprocess.run(["knotc", "zone-commit", f"{domain}"])
    return f"Knot DNS config created for {domain}"


@app.route("/dns/record/<domain>", methods=["POST"])
def add_record(domain):
	record_type = request.form["record_type"]
	record_name = request.form["record_name"]
	record_ttl = request.form["record_ttl"]
	record_value = request.form["record_value"]


	subprocess.run(["knotc", "zone-begin", f"{domain}"])
	subprocess.run(["knotc", "zone-set", f"{domain}.", record_name, record_ttl, record_type, record_value])
	subprocess.run(["knotc", "zone-commit", f"{domain}"])
	return f"New record added to {domain}"


@app.route("/dns/config/<domain>", methods=["DELETE"])
def delete_config(domain):
	#subprocess.run(["rm", "-rvf", "/var/lib/knot/" f"{domain}.zone",])
	#subprocess.run(["knotc", "zone-begin", f"{domain}"])
	#subprocess.run(["knotc", "zone-unset", f"{domain}."])
	#subprocess.run(["knotc", "zone-commit", f"{domain}"])
	#subprocess.run(["knotc", "zone-delete", f"{domain}"])
	return f"Knot DNS config/zone deleted for {domain}"



@app.route("/dns/record/<domain>", methods=["DELETE"])
def delete_record(domain):
	record_name = request.form["record_name"]


	subprocess.run(["knotc", "zone-begin", f"{domain}"])
	subprocess.run(["knotc", "zone-unset", f"{domain}.", record_name])
	subprocess.run(["knotc", "zone-commit", f"{domain}"])	
	return f"Record deleted from {domain}"



if __name__ == "__main__":
    app.run(debug=True)
