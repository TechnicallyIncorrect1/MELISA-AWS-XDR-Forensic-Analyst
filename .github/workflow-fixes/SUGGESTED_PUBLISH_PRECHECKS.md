# Suggested publish workflow pre-checks (SUGGESTED_PUBLISH_PRECHECKS.md)

# Example pre-check snippet to include near the start of publish workflows to fail early if secrets are missing.

```yaml
- name: Verify required secrets
  run: |
    missing=false
    if [ -z "${{ secrets.MAVEN_CENTRAL_USERNAME }}" ]; then echo "MAVEN_CENTRAL_USERNAME missing"; missing=true; fi
    if [ -z "${{ secrets.MAVEN_CENTRAL_PASSWORD }}" ]; then echo "MAVEN_CENTRAL_PASSWORD missing"; missing=true; fi
    if [ -z "${{ secrets.GPG_PRIVATE_KEY }}" ]; then echo "GPG_PRIVATE_KEY missing"; missing=true; fi
    if [ "$missing" = true ]; then echo 'One or more required secrets are missing. Please add them to Settings → Secrets → Actions.'; exit 1; fi
```

Place this step in your publish workflows and update the secret names to match your workflow definitions.
