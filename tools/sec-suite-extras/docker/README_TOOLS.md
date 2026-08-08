# Append: Additional Tools Docs

The following tools have docker images and documentation included in the tools/sec-suite-extras/docker directory:
- mitmproxy (containerized; manual start required for interception)
- impacket (python client + scripts)
- responder (image provided; DO NOT run on shared networks)
- twint, sherlock, knockpy, fierce (images for offline/help usage)
- shodan python client image (requires SHODAN_API_KEY to use)
- cryptohack image for offline crypto challenges

All images are deliberately configured to avoid running intrusive actions automatically. Use the run_tools_extended.sh script to collect safe/help outputs. For active scans or attacks, run commands manually inside the appropriate container and only target in-scope/lab assets.
