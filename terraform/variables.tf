variable "gcp_project" {
  description = "A GCP project"
  type        = string
  default     = "prollm-translator"
}

variable "gcp_region" {
  description = "A GCP region"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "A GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "google_compute_instance_name" {
  description = "The name of the prollm-translator compute instance"
  type        = string
  default     = "prollm-translator"
}

variable "google_compute_instance_image" {
  description = "A Google Compute Instance image"
  type        = string
  default     = "projects/debian-cloud/global/images/debian-11-bullseye-v20230912"
}
