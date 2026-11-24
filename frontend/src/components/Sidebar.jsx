
function Sidebar({ activeTab, onNavigate }) {
  const menuItems = [
    'Overview',
    'GIS Map',
    'Analytics',
    'Historical Data',
    'Settings',
  ]

  return (
    <aside className="sidebar">
      <h2>TerraSpectra</h2>

      <nav>
        {menuItems.map((item) => (
          <button
            key={item}
            type="button"
            className={`sidebar-link ${
              activeTab === item ? 'active' : ''
            }`}
            onClick={() => onNavigate(item)}
          >
            {item}
          </button>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar