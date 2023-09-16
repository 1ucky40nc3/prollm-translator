# This code is compatible with Terraform 4.25.0 and versions that are backwards compatible to 4.25.0.
# For information about validating this Terraform code, see https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build#format-and-validate-the-configuration

# Local enviroment variables from a `.env` file at the root dir
locals {
  envs = { for tuple in regexall("(.*)=(.*)", file("../.env")) : tuple[0] => sensitive(tuple[1]) }
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.82.0"
    }
  }
}

provider "google" {
  credentials = file("key.json")

  project = var.gcp_project
  region  = var.gcp_region
  zone    = var.gcp_zone
}

resource "google_compute_instance" "prollm-translator" {
  boot_disk {
    auto_delete = true
    device_name = var.google_compute_instance_name

    initialize_params {
      image = var.google_compute_instance_image
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src = "vm_add-tf"
    # Install Ops Agent for Monitoring and Logging
    goog-ops-agent-policy = "v2-x86-template-1-1-0"
  }

  machine_type = "e2-micro"

  metadata = {
    enable-osconfig = "TRUE"
    # Add a manually generated SSH key
    ssh-keys = "${local.envs["SSH_USERNAME"]}:${file("../.ssh/id_rsa.pub")}"
  }

  name = var.google_compute_instance_name

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    # Select the default subnetwork the project's region
    subnetwork = "projects/${var.gcp_project}/regions/${var.gcp_region}/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = true
    enable_vtpm                 = true
  }

  zone = var.gcp_zone
}
