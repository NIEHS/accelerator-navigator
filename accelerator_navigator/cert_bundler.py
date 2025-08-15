import certifi, pathlib, os, ssl


def bundle_certs(input_cert_file:str):
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the path relative to the script
    # file_path = os.path.join(script_dir, "resources", "NIH-DPKI-ROOT-1A.pem")
    ORG_CA = os.path.join(script_dir, "resources", "chain.pem")
    bundle = os.path.join(script_dir, "resources", "newchain.pem")

    org_chain = pathlib.Path(__file__).resolve().parent / "resources" / "chain.pem"
    bundle = pathlib.Path(__file__).resolve().parent / "resources" / "combined-ca.pem"

    bundle.write_bytes(
        pathlib.Path(certifi.where()).read_bytes() + b"\n" + org_chain.read_bytes()
    )

    os.environ["SSL_CERT_FILE"] = str(bundle)



