function StatCard({ title, value, description, icon }) {
    return (
        <div className="stat-card">
            <div className="stat-top">
                <span className="stat-title">{title}</span>
                {icon && <div className="stat-icon-wrapper">{icon}</div>}
            </div>

            <div className="stat-value">{value}</div>

            {description && (
                <p className="stat-description">{description}</p>
            )}
        </div>
    );
}

export default StatCard;