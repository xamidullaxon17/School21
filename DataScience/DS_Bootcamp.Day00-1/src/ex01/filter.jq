.items[] | select(.name | test("data scientist|scientist"; "i")) | "\"\(.id)\",\"\(.created_at)\",\"\(.name)\",\"\(.has_test)\",\"\(.alternate_url)\""
