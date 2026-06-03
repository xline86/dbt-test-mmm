use role accountadmin;

create role if not exists dbt_test_mmm_role;

create warehouse if not exists dbt_test_mmm_wh
    warehouse_size = xsmall
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true;

create database if not exists dbt_test_mmm_db;
grant usage on warehouse dbt_test_mmm_wh to role dbt_test_mmm_role;
grant ownership on database dbt_test_mmm_db to role dbt_test_mmm_role;

create user if not exists mmm
    login_name = 'mmm'
    default_role = dbt_test_mmm_role
    default_warehouse = dbt_test_mmm_wh
    comment = 'dbt-test-mmmの開発用ユーザー。accountadminを持っていないユーザーを作りたかった';

alter user mmm
    set rsa_public_key = '<% dbt_user_rsa_public_key %>';

grant role dbt_test_mmm_role to user mmm;
grant role dbt_test_mmm_role to role sysadmin;
