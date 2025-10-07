## Database Design & Operational Best Practices

This document summarizes database design, performance, reliability, and operational patterns relevant to the Smart Digital Food Menu project.

### Quick contract
- Inputs: SQL queries, application workload (reads/writes), schema DDL
- Outputs: predictable latency, correct results, high availability, and recoverability
- Error modes: connection failures, long-running queries, replica lag, schema drift

### Table Indexing
- Use B-tree indexes on columns used in WHERE, JOIN and ORDER BY clauses.
- Create composite indexes for common multi-column filters (e.g. (category_id, food_name)).
- Consider covering indexes to satisfy SELECT queries entirely from the index and avoid lookups.
- Avoid over-indexing: each index increases write cost and storage.
- Use partial/filtered indexes (where supported) for sparse columns.

Example (MySQL):
CREATE INDEX idx_food_category_name ON food_items (category_id, food_name);

### Join Queries
- Prefer joins that leverage indexed join keys. Ensure joined columns are indexed on the child side.
- Use explicit JOINs (INNER/LEFT) instead of comma joins for readability and control.
- For existence checks, use EXISTS instead of COUNT(*) when you only need presence.
- Be careful with large CROSS JOINs and cartesian products.

Tip: run EXPLAIN/EXPLAIN ANALYZE on complex joins and look for full table scans.

### Query Optimization Best Practices
- Push filters down early and select only required columns (avoid SELECT *).
- Use LIMIT for paging and range queries; prefer keyset pagination for large datasets.
- Batch writes/inserts to reduce round-trips and transaction overhead.
- Use prepared statements and parameterized queries to improve plan reuse and security.
- Cache frequently accessed but rarely changing data (e.g., health_conditions) in the application or an external cache (Redis).

### DB Connection & Pooling
- Use connection pools rather than creating a connection per request.
- Configure idle timeout, max connections and validation queries (e.g., SELECT 1).
- For Python with mysql-connector or pymysql, use connection pooling libraries or SQLAlchemy's Engine.

Example (mysql.connector pooling):
from mysql.connector import pooling
pool = pooling.MySQLConnectionPool(pool_name='app_pool', pool_size=10, **MYSQL_CONFIG)
conn = pool.get_connection()

### Multi-DB & Read/Write Pools
- Multi-DB approaches:
  - Primary-replica (one writer, many readers)
  - Sharding (by user_id, region) for horizontal scale
  - Multi-tenant databases (schema-per-tenant or shared schema)
- Read pool: route read-only traffic to replicas. Be mindful of replica lag and stale reads.
- Write pool: route writes to the primary. Centralize schema changes and migrations to the primary with careful rollout.

Routing strategy: the application should be able to choose a read or write pool per operation. Keep session/transaction affinity for transactional workflows.

### Singleton Connection Manager Pattern
- Implement a singleton or factory that exposes pooled connections to the app and centralizes config and monitoring.
- Ensure graceful shutdown closes pools and drains connections.

### Normalization & When to Denormalize
- Normalize to 3NF to avoid data anomalies for transactional tables (users, health_conditions, food_items).
- Denormalize for read-heavy queries where joins are costly; maintain via application logic or DB triggers.

### Fallback / Retry (Resilience)
- Use idempotent retries with exponential backoff and jitter for transient network/database errors.
- Limit retries and fail fast for non-idempotent write operations or use distributed transactions where needed.

Pseudocode:
retry = 0
while retry < MAX:
  try: do_db_op(); break
  except TransientError: sleep(exp_backoff(retry)); retry += 1

### High Availability
- Use automated failover: keep a hot standby and orchestrate failover with a reliable coordinator (e.g., MHA, Orchestrator, Patroni for Postgres).
- Health checks, quorum-based decision making, and automated DNS updates or proxy reconfiguration are crucial.
- Keep replicas geographically distributed to survive AZ failures.

### Backup & Recovery
- Regularly take full backups and frequent incremental backups. Test restores routinely.
- For MySQL: use logical backups (mysqldump) for schema and data, and physical backups (Percona XtraBackup) for large datasets.
- For point-in-time recovery (PITR), enable binary log archiving and keep retention policies consistent with RTO/RPO.

### Operational Checklist
- Monitor: query latency, slow queries, replica lag, connection pool saturation, disk usage.
- Alerts: long-running migrations, backup failures, replication breaks.
- Run schema migrations safely (zero downtime patterns: copy tables, backfill, swap pointer).

### Security & Credentials
- Keep credentials out of source control. Use environment variables or a secrets manager (Vault, AWS Secrets Manager).
- Use least privilege accounts for applications.

### Next Steps for this Project
- Add a small connection-pool wrapper in `database_config.py` to expose a singleton pool and health-check endpoints.
- Add monitoring dashboards (Grafana + Prometheus) and automated backups to CI/CD or a cron job.

References & further reading
- Use the DB vendor docs and performance guides for MySQL/Postgres. Look up "EXPLAIN ANALYZE", "index usage", and "connection pooling" for deeper dives.
