create table stp (
    name text primary key,
    title text,
    capacity text,
    section text
);

create table metric (
    name text primary key,
    title text,
    lower_limit float,
    upper_limit float,
    unit text
);


create table water_quality (
    stp_name text,
    timestamp text,
    ph float,
    temperature float,
    ammonical_nitrogen float,
    total_nitrogen float,
    cod float,
    bod float,
    tss float,
    color float,
    dissolved_oxygen float,
    updated_on text
);

create index water_quality_stp_name_idx on water_quality(stp_name);
create index water_quality_updated_on_idx on water_quality(updated_on);
